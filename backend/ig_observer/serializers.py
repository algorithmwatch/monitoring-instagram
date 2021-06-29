import logging
from rest_framework import serializers, exceptions
from data_donors.models import Donor
from . import models

logger = logging.getLogger(__name__)


class IgUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IgUser
        fields = [
            'id',
            'ig_username',
            'ig_biography',
            'ig_full_name',
            'ig_profile_pic',
        ]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = [
            'id',
            'name',
            'active',
            'description',
            'default_for_locale',
        ]


class IgUserFollowedBySerializer(serializers.ModelSerializer):
    ig_username = serializers.CharField(write_only=True)
    author = serializers.CharField(write_only=True)

    class Meta:
        model = models.IgUserFollowedBy
        fields = [
            'id',
            'ig_username',
            'author',
            'count',
        ]

    def create(self, validated_data):
        ig_username = validated_data.pop('ig_username')
        try:
            author = validated_data.pop('author')
            donor = Donor.objects.get_by_ig_username(author)
        except Donor.DoesNotExist:
            raise exceptions.NotFound()
        ig_user = models.IgUser.objects.get(ig_username=ig_username)
        validated_data['ig_user'] = ig_user
        validated_data['created_by'] = donor
        return super().create(validated_data)
