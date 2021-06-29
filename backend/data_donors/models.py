from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from ig_observer.models import IgPost, IgUser
from .utils import get_anonymous_id_from_username


class Donor(models.Model):
    ig_donor_id = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    following = models.ManyToManyField(IgUser, related_name='followers')
    last_status = models.BooleanField()
    last_status_changed = models.DateTimeField()
    version = models.CharField(max_length=6, null=True, blank=True)
    browser = models.CharField(max_length=7, null=True, blank=True)
    display_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        if self.display_name:
            return self.display_name
        else:
            return self.ig_donor_id

    def save(self, *args, **kwargs):
        # set last_status_changed
        if self.pk:
            previous_status = Donor.objects.get(pk=self.pk).last_status
            if previous_status != self.last_status:
                self.last_status_changed = timezone.now()
        if not self.last_status_changed:
            self.last_status_changed = timezone.now()
        super().save(*args, **kwargs)

    class DonorManager(models.Manager):
        def get_by_ig_username(self, username):
            donor_id = get_anonymous_id_from_username(username)
            return self.get(ig_donor_id=donor_id)

    objects = DonorManager()


class DataDonation(models.Model):
    DONATION_TYPES = (
        ('FEED', 'Feed'),
        ('EXPLORE', 'Explore'),
    )
    created = models.DateTimeField(auto_now_add=True)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, null=True)
    donation_type = models.CharField(choices=DONATION_TYPES,
                                     max_length=7,
                                     default='FEED')
    ig_posts_seen = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.donor and self.donor.ig_donor_id or 'anonynous'} on {self.created}"


class Encounter(models.Model):
    data_donation = models.ForeignKey(DataDonation, on_delete=models.CASCADE)
    ig_post = models.ForeignKey(IgPost,
                                verbose_name='Instagram Post',
                                on_delete=models.CASCADE)
    position_in_list = models.IntegerField(
        help_text="Position in DataDonation ig_posts_seen list")
    comments_count = models.IntegerField(null=True)
    likes_count = models.IntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ig_post', 'data_donation'],
                                    name='unique_post_by_donation'),
        ]


class DataDonationError(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.TextField(blank=True, null=True)
    traceback = models.TextField(blank=True, null=True)
    payload = JSONField(blank=True, null=True)


class DonorFollowing(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    following_ig_username = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Donor is following'
        verbose_name_plural = 'Donor is following'
        constraints = [
            models.UniqueConstraint(fields=['donor', 'following_ig_username'],
                                    name='unique_donor_following'),
        ]

    def __str__(self):
        return f"{self.donor} is following {self.following_ig_username}"
