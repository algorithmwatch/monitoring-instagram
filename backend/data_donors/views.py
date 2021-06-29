from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.core import serializers as djangoSerializer
from . import serializers
from . import models
from .utils import get_anonymous_id_from_username


class DataDonationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ## Allow to donors to send their data
    """
    queryset = models.DataDonation.objects.all()
    serializer_class = serializers.DataDonationSerializer


class DataDonorViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ## Allow to donors to register and claim who they are following
    """
    queryset = models.Donor.objects.all()
    serializer_class = serializers.DonorSerializer

    def create(self, request, *args, **kwargs):
        serializer = None
        ig_username = request.data.get('ig_username')
        if not ig_username:
            raise Exception('no username')
        instance = models.Donor.objects.filter(
            ig_donor_id=get_anonymous_id_from_username(ig_username)).first()
        if instance:
            serializer = self.get_serializer(instance, data=request.data)
        if not serializer:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


def export_view(request):
    '''
    Export the given user data as a json file
    '''
    username = request.GET.get('username')
    if not username:
        return HttpResponseBadRequest('Username required')
    donor = models.Donor.objects.get_by_ig_username(username)
    donations = models.DataDonation.objects.filter(donor=donor)
    enconters = models.Encounter.objects.filter(data_donation__donor=donor)
    payload = djangoSerializer.serialize(
        'json',
        [donor, *donations, *enconters],
        indent=2,
        use_natural_primary_keys=True,
        use_natural_foreign_keys=True,
    )
    response = HttpResponse(payload)
    response[
        'Content-Disposition'] = 'attachement; filename=monitoring-ig.exported.json'
    return response
