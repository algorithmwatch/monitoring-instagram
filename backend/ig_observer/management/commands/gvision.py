from django.core.management.base import BaseCommand
from ig_observer.models import IgImage


class Command(BaseCommand):
    help = 'Fetch from Google Vision metadata for all the images'

    def handle(self, *args, **options):
        counter = 0
        # image not yet analyzed
        query = IgImage.objects.filter(gvisionanalyse__isnull=True)
        # analyze only posts from donor's feed or scrapper (not EXPLORE)
        query = query.filter(
            ig_post__encounter__data_donation__donation_type='FEED'
        ) | query.filter(ig_post__encounter__isnull=True)
        query = query.distinct('id')
        for image in query:
            self.stdout.write(f'create_gvision_analyse for {image}')
            image.create_gvision_analyse()
            counter += 1
        self.stdout.write(f'created {counter} analyses', self.style.SUCCESS)
