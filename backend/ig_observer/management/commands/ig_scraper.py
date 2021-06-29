import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import F
from ig_observer.models import IgUser, IgPost, IgEngagements
from ig_observer.ig_scraper import scrape_post, PrivateAccountException, RenamedAccountException

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Scrape all IG profiles and their posts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep-going',
            action='store_true',
            help='Keep going even if it find an existing post',
        )
        parser.add_argument(
            '--new-posts',
            action='store_true',
            help='Fetch new posts',
        )
        parser.add_argument(
            '--likes',
            action='store_true',
            help='Fetch likes and comments for posts younger than 2 days',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Ignore skip based on time',
        )

    def handle(self, *args, **options):
        current_hour_mod_4 = timezone.datetime.now().hour % 4
        skip = current_hour_mod_4 in [0, 2]
        if skip and not options['force']:
            self.stdout.write('We skip than one.')
            return None
        reverse = current_hour_mod_4 == 3
        self.stdout.write('reverse: %s' % reverse)
        if options['new_posts']:
            self.fetch_new_posts(options['keep_going'])
        if options['likes']:
            self.likes_and_comments(reverse=reverse)

    def fetch_new_posts(self, keep_going):
        # get new posts
        self.stdout.write('get new posts')
        users = IgUser.objects.filter(
            is_active=True, project__active=True).order_by(
                F('last_scrape').asc(nulls_first=True))
        users_total = users.count()
        total_errors_in_a_row = 0
        for user_count, user in enumerate(users, 1):
            self.stdout.write(
                f'{user.ig_username} {user_count}/{users_total} | Last scrape: {user.last_scrape}'
            )
            # pylint: disable=broad-except
            try:
                user.scrape_media(keep_going=keep_going)
                total_errors_in_a_row = 0
            except RenamedAccountException as error:
                logger.error("%s. Disabling it. [LOOK_AT_THAT,ADMIN]", error)
                user.is_active = False
                user.save()
            except PrivateAccountException:
                logger.error(
                    "The account %s seems to be private. Disabling it. [LOOK_AT_THAT,ADMIN]",
                    user.ig_username)
                user.is_active = False
                user.save()
            except Exception:
                total_errors_in_a_row = total_errors_in_a_row + 1
                logger.exception('fetching user %s has failed. %d in a row',
                                 user, total_errors_in_a_row)
                if total_errors_in_a_row >= 3:
                    raise Exception('Failed 3 times in a row. We stop there.')

    def likes_and_comments(self, reverse):
        # get likes and comments for every posts younger than 48h
        self.stdout.write(
            'get likes and comments for every posts younger than 48h')
        two_days_ago = timezone.now() - timezone.timedelta(hours=48)
        posts = IgPost.objects.filter(
            created__gt=two_days_ago,
            deleted_by_user=False,
            ig_user__is_active=True,
            ig_user__project__active=True).order_by('id')
        total_errors_in_a_row = 0
        if reverse:
            posts = posts.reverse()
        for i, post in enumerate(posts):
            self.stdout.write(f"{post} {i + 1}/{posts.count()}")
            data = None
            try:
                data = scrape_post(post.ig_shortcode)
                if data:
                    likes_count = data['edge_media_preview_like']['count']
                    comments_count = data['edge_media_to_parent_comment'][
                        'count']
                    comments = data['edge_media_to_parent_comment']['edges']
                    IgEngagements.objects.create(
                        ig_post=post,
                        comments_count=comments_count,
                        comments=comments,
                        likes_count=likes_count,
                    )
                else:
                    logger.info(
                        'Post %s has been deleted. It won\'t be checked anymore',
                        post)
                    post.deleted_by_user = True
                    post.save()
                total_errors_in_a_row = 0
            except Exception as ex:  #  pylint: disable=broad-except
                total_errors_in_a_row = total_errors_in_a_row + 1
                logger.exception(ex)
                if data:
                    logger.info("data: %s", data)
                if total_errors_in_a_row >= 3:
                    raise Exception('Failed 3 times in a row. We stop there.')
