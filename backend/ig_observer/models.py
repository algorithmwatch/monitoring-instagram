import json
import logging
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import datetime, make_aware
from django.db import transaction
from django.conf import settings
from adminsortable.models import SortableMixin
from requests.models import HTTPError
from .gvision import analyse_image, GVisionException
LOGGER = logging.getLogger(__name__)


class IgUserFollowedBy(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('data_donors.Donor',
                                   on_delete=models.CASCADE)
    ig_user = models.ForeignKey('IgUser', on_delete=models.CASCADE)
    count = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Monitored User is followed by'
        verbose_name_plural = 'Monitored User is followed by'

    def __str__(self):
        return f'{self.ig_user} has {self.count} followers'


class IgEngagements(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    ig_post = models.ForeignKey('IgPost', on_delete=models.CASCADE)
    comments_count = models.IntegerField(null=True)
    comments = JSONField(blank=True, null=True)
    likes_count = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Engagements'
        verbose_name_plural = 'Engagements'

    def __str__(self):
        return f'{self.ig_post}: {self.likes_count} likes and {self.comments_count} comments on {self.created}'

    def get_absolute_url(self):
        return f'https://instagram.com/p/{self.ig_post.ig_shortcode}'


class IgPostManager(models.Manager):
    def get_or_create_post(self, ig_id, owner, node, created_by_donor=False):
        post_instance = self.filter(ig_id=ig_id).first()
        created = False
        if not post_instance:
            created = True
            with transaction.atomic():
                post_instance = self.create(
                    ig_user=owner,
                    ig_id=node['id'],
                    ig_shortcode=node['shortcode'],
                    ig_media_caption='\n'.join([
                        edge['node']['text']
                        for edge in node['edge_media_to_caption']['edges']
                    ]),
                    ig_taken_at_timestamp=make_aware(
                        datetime.utcfromtimestamp(node['taken_at_timestamp'])),
                    ig_type=node['__typename'],
                    created_by_donor=created_by_donor,
                )
                if node['__typename'] == 'GraphImage':
                    IgImage.objects.create(ig_post=post_instance,
                                           image_url=node['display_url'])
                elif node['__typename'] == 'GraphSidecar':
                    if 'edge_sidecar_to_children' in node:
                        for edge in node['edge_sidecar_to_children']['edges']:
                            node = edge['node']
                            IgImage.objects.create(
                                ig_post=post_instance,
                                image_url=node['display_url'])
        return post_instance, created


class IgPost(models.Model):
    IG_TYPE_CHOICES = (
        ('GraphImage', 'GraphImage'),
        ('GraphSidecar', 'GraphSidecar'),
        ('GraphVideo', 'GraphVideo'),
    )
    objects = IgPostManager()
    created = models.DateTimeField(auto_now_add=True)
    ig_user = models.ForeignKey('IgUser', on_delete=models.CASCADE, null=True)
    ig_username = models.CharField(max_length=255, null=True)
    ig_id = models.CharField(max_length=50, unique=True)
    ig_shortcode = models.CharField(max_length=255, unique=True)
    ig_taken_at_timestamp = models.DateTimeField()
    ig_type = models.CharField(choices=IG_TYPE_CHOICES, max_length=15)
    ig_media_caption = models.TextField(blank=True, null=True)
    created_by_donor = models.BooleanField(default=False)
    deleted_by_user = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Post'

    def __str__(self):
        return f'{self.ig_type}:{self.ig_shortcode}  by {self.ig_user or self.ig_username}'

    def get_absolute_url(self):
        return f'https://instagram.com/p/{self.ig_shortcode}'

    def natural_key(self):
        return self.get_absolute_url()


class IgImage(models.Model):
    ig_post = models.ForeignKey(IgPost, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=255 * 2)

    class Meta:
        verbose_name = 'Image'

    def __str__(self):
        return f"{self.image_url[:50]}... ({self.ig_post})"

    def create_gvision_analyse(self, *args, **kwargs):
        try:
            analyse = analyse_image(self.image_url, *args, **kwargs)
            GVisionAnalyse.objects.create(ig_image=self, analyse=analyse)
        except GVisionException as error:
            LOGGER.warning('Gvision error: %s', error)


class GVisionAnalyse(models.Model):
    ig_image = models.OneToOneField(IgImage, on_delete=models.CASCADE)
    analyse = JSONField()
    created = models.DateTimeField(auto_now_add=True)


class Project(SortableMixin):
    name = models.CharField('Project name', max_length=255)
    active = models.BooleanField(default=True)
    description = models.TextField('Project description', null=True)
    default_for_locale = models.CharField(
        help_text=
        'A list of languages tag such as "en-US" or "fr", coma separated',
        max_length=5,
        blank=True,
        null=True)
    order = models.PositiveIntegerField(default=0,
                                        editable=False,
                                        db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class IgUser(models.Model):
    SEX = (
        (
            'F',
            'Female',
        ),
        (
            'M',
            'Male',
        ),
    )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    ig_username = models.CharField(max_length=50, unique=True, db_index=True)
    sex = models.CharField(max_length=1, choices=SEX, blank=True, null=True)
    ig_id = models.CharField(max_length=50,
                             unique=True,
                             db_index=True,
                             blank=True,
                             null=True)
    ig_biography = models.TextField(blank=True, null=True)
    ig_business_category_name = models.CharField(max_length=100,
                                                 blank=True,
                                                 null=True)
    ig_full_name = models.CharField(max_length=255, blank=True, null=True)
    ig_profile_pic = models.ImageField(upload_to='profile_pic/',
                                       blank=True,
                                       null=True)
    ig_is_business_account = models.BooleanField(blank=True, null=True)
    last_scrape = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Monitored User'

    def __str__(self):
        return '@' + self.ig_username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if settings.COMPLETE_PROFILE_ON_CREATION:
            self.scrape_profile()

    def scrape_media(self, *args, **kwargs):
        from .ig_scraper import scrape_media
        scrape_media(self, *args, **kwargs)

    def scrape_profile(self, *args, **kwargs):
        from .ig_scraper import get_or_complete_user_by_ig_username
        get_or_complete_user_by_ig_username(self, *args, **kwargs)
