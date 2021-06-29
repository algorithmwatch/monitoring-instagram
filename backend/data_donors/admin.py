from django.contrib import admin
from . import models


@admin.register(models.Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'last_status',
        'last_status_changed',
        'updated',
        'created',
        'version',
        'browser',
    ]
    list_filter = ['last_status']
    search_fields = ['ig_donor_id']


@admin.register(models.DataDonation)
class DataDonationAdmin(admin.ModelAdmin):
    class EncounterInlined(admin.StackedInline):
        model = models.Encounter
        readonly_fields = [
            'ig_post', 'position_in_list', 'comments_count', 'likes_count'
        ]
        extra = 0

        def has_add_permission(self, req, obj):
            return False

        def has_delete_permission(self, req, obj):
            return False

    list_display = [
        'donor',
        'donation_type',
        'encounter_count',
        'ig_posts_seen',
        'created',
    ]
    search_fields = ['id', 'donor__ig_donor_id']
    list_filter = ['donor__browser', 'donation_type']
    date_hierarchy = 'created'
    inlines = [EncounterInlined]

    def encounter_count(self, obj):
        return obj.encounter_set.all().count()


@admin.register(models.Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'ig_post_shortcode',
        'position_in_list',
        'data_donation__donor',
        'data_donation__created',
        'data_donation__posts_seen',
    ]
    search_fields = [
        'id',
        'data_donation__id',
        'ig_post__id',
        'data_donation__donor__id',
    ]
    readonly_fields = [
        'ig_post', 'position_in_list', 'comments_count', 'likes_count'
    ]
    date_hierarchy = 'data_donation__created'
    list_filter = [
        ('ig_post__ig_user', admin.RelatedOnlyFieldListFilter),
    ]
    autocomplete_fields = [
        'data_donation',
        'ig_post',
    ]

    def data_donation__created(self, obj):
        return obj.data_donation.created

    def data_donation__donor(self, obj):
        return obj.data_donation.donor and obj.data_donation.donor.ig_donor_id

    data_donation__donor.short_description = "Data donor"
    data_donation__created.admin_order_field = 'data_donation__created'

    def data_donation__posts_seen(self, obj):
        return obj.data_donation.ig_posts_seen

    def ig_post_shortcode(self, obj):
        return obj.ig_post.ig_shortcode


@admin.register(models.DataDonationError)
class DataDonationErrorAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'created',
    ]
    date_hierarchy = 'created'


@admin.register(models.DonorFollowing)
class DonorFollowingAdmin(admin.ModelAdmin):
    list_display = [
        'donor',
        'following_ig_username',
        'created',
    ]
    search_fields = ['donor__ig_donor_id', 'following_ig_username']
    date_hierarchy = 'created'
