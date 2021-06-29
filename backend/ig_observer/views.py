from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from . import serializers
from . import models


class ThreeResultsPagination(PageNumberPagination):
    page_size = 3


class IgUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ## Allow to donors to get a a list of account to follow
    """
    queryset = models.IgUser.objects.filter(is_active=True).filter(
        project__id=1).order_by("?")[:3]
    serializer_class = serializers.IgUserSerializer


class IgUserViewSet2(IgUserViewSet):
    """
    ## Allow to donors to get a a list of account to follow
    """
    queryset = models.IgUser.objects.filter(is_active=True).order_by("?")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']
    pagination_class = ThreeResultsPagination


class ProjectViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    ## Allow to donors to get a a list of all the projects
    """
    queryset = models.Project.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active']
    serializer_class = serializers.ProjectSerializer


class IgUserFollowedByViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    """
    ## Allow to donors to send follower count
    """
    queryset = models.IgUserFollowedBy.objects.all()
    serializer_class = serializers.IgUserFollowedBySerializer
