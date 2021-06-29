import traceback
import logging
from django.utils.timezone import datetime, make_aware
from rest_framework import serializers
from django.db import transaction
from ig_observer.models import IgImage, IgUser, IgPost
from . import models
from .utils import get_anonymous_id_from_username

logger = logging.getLogger(__name__)


class DonorSerializer(serializers.ModelSerializer):

    ig_username = serializers.CharField(write_only=True)

    class Meta:
        model = models.Donor
        fields = [
            "ig_username", "following", "last_status", "version", "browser"
        ]

    def create(self, validated_data):
        ig_username = validated_data.pop('ig_username')
        validated_data['ig_donor_id'] = get_anonymous_id_from_username(
            ig_username)
        return super().create(validated_data)


class ActualDataDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DataDonation
        fields = ["__all__"]


class DataDonationSerializer(serializers.Serializer):
    data = serializers.JSONField(write_only=True)
    data_source = serializers.ChoiceField(
        (
            ('__additionalData', 'Feed (window.__additionalData)'),
            ('explore', 'Explore'),
        ),
        write_only=True,
    )

    def create(self, validated_data):
        data = validated_data.pop('data')
        data_source = validated_data.pop('data_source')
        parser = PARSERS.get(data_source)
        if parser:
            try:
                instance = parser(data)
                return ActualDataDonationSerializer(instance)
            except Exception as error:
                models.DataDonationError.objects.create(
                    name=f"{type(error)} - {error}",
                    traceback=traceback.format_exc(),
                    payload={
                        'data_source': data_source,
                        'data': data
                    })
                raise error
        else:
            raise serializers.ValidationError()


def ingest_from_additional_data(data):
    # get the donor
    donor_instance = models.Donor.objects.get_by_ig_username(data['username'])
    # get the accounts he is following
    tracked_usernames_in_db_by_username = {
        u.ig_username: u
        for u in donor_instance.following.all()
    }
    with transaction.atomic():
        # create the donation object
        donation_instance = models.DataDonation.objects.create(
            donor=donor_instance,
            ig_posts_seen=len(data['edge_web_feed_timeline']['edges']),
        )
        # for every post which has the owner tracked
        for position, edge in enumerate(
                data['edge_web_feed_timeline']['edges']):
            node = edge['node']
            # if this is a proper post with an owner
            if 'owner' in node:
                # if the post owner in monitored
                if node['owner'][
                        'username'] in tracked_usernames_in_db_by_username.keys(
                        ):
                    # checks if the related post exists, or creates it
                    ig_post_instance, _created = IgPost.objects.get_or_create_post(
                        node['id'],
                        owner=tracked_usernames_in_db_by_username[
                            node['owner']['username']],
                        node=node,
                        created_by_donor=True)
                    # create the Encounter object
                    models.Encounter.objects.create(
                        data_donation=donation_instance,
                        ig_post=ig_post_instance,
                        position_in_list=position,
                        comments_count=node['edge_media_preview_comment']
                        ['count'],
                        likes_count=node['edge_media_preview_like']['count'],
                    )
                # create the DonorFollowing object if it doesn't exist yet
                models.DonorFollowing.objects.get_or_create(
                    donor=donor_instance,
                    following_ig_username=get_anonymous_id_from_username(
                        node['owner']['username']))
        return donation_instance


def ingest_explore_data(data):
    def _get_or_create_post(media):
        IG_TYPES = {
            1: 'GraphImage',
            8: 'GraphSidecar',
            # 2: 'GraphVideo',
        }
        existing = IgPost.objects.filter(ig_id=media['pk']).first()
        if existing:
            return existing
        ig_type = IG_TYPES.get(media['media_type'])
        known_author = IgUser.objects.filter(
            ig_id=str(media['user']['pk'])).last()
        if ig_type:
            caption = None
            if media.get('caption'):
                caption = media['caption']['text']
            post = IgPost.objects.create(
                ig_user=known_author,
                ig_username=media['user']['username'],
                ig_id=media['pk'],
                ig_shortcode=media['code'],
                ig_taken_at_timestamp=make_aware(
                    datetime.utcfromtimestamp(media['taken_at'])),
                ig_type=ig_type,
                ig_media_caption=caption,
                created_by_donor=True,
            )
            if ig_type == 'GraphImage':
                IgImage.objects.create(
                    ig_post=post,
                    image_url=media['image_versions2']['candidates'][0]['url'],
                )
            elif ig_type == 'GraphSidecar':
                for image in media['carousel_media']:
                    IgImage.objects.create(
                        ig_post=post,
                        image_url=image['image_versions2']['candidates'][0]
                        ['url'],
                    )
            return post

    def find_item(obj, key):
        if isinstance(obj, dict):
            if key in obj:
                yield obj[key]
            for value in obj.values():
                yield from find_item(value, key)
        elif isinstance(obj, list):
            for value in obj:
                yield from find_item(value, key)

    def get_media_list(data):
        return list(find_item(data, 'media'))

    # get the donor
    donor_instance = models.Donor.objects.get_by_ig_username(
        data['ig_username'])
    media_list = get_media_list(data['payload'])

    with transaction.atomic():
        donation = models.DataDonation.objects.create(
            donor=donor_instance,
            donation_type='EXPLORE',
            ig_posts_seen=len(media_list),
        )

        for index, media in enumerate(media_list):
            # checks if the related post exists, or creates it
            ig_post_instance = _get_or_create_post(media)
            if ig_post_instance:
                # create the Encounter object
                models.Encounter.objects.create(
                    data_donation=donation,
                    ig_post=ig_post_instance,
                    position_in_list=index,
                    comments_count=media.get('comment_count'),
                    likes_count=media.get('like_count'),
                )


PARSERS = {
    '__additionalData': ingest_from_additional_data,
    'explore': ingest_explore_data,
}
