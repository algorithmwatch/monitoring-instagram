import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.contrib import admin
from django.utils.safestring import mark_safe
from adminsortable.admin import SortableAdmin
from modeltranslation.admin import TranslationAdmin
from . import models
from .filters import RacyFilter


@admin.register(models.IgUserFollowedBy)
class IgUserFollowedByAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'ig_user',
        'count',
        'created_by',
        'created',
    ]


@admin.register(models.IgEngagements)
class IgEngagementsAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'ig_post',
        'likes_count',
        'comments_count',
    ]
    autocomplete_fields = ['ig_post']
    date_hierarchy = 'created'


@admin.register(models.Project)
class ProjectAdmin(SortableAdmin, TranslationAdmin):
    list_display = [
        '__str__',
        'active',
        'default_for_locale',
        'order',
    ]
    list_filter = ['active', 'default_for_locale']


@admin.register(models.IgPost)
class IgPostAdmin(admin.ModelAdmin):
    list_display = [
        'ig_shortcode',
        'ig_user',
        'ig_username',
        'ig_taken_at_timestamp',
        'ig_type',
        'created',
        'deleted_by_user',
    ]
    readonly_fields = [
        'ig_id',
        'ig_shortcode',
        'ig_user',
        'ig_username',
        'ig_taken_at_timestamp',
        'ig_type',
        'created',
        'created_by_donor',
        'ig_media_caption',
        'deleted_by_user',
    ]
    list_filter = [
        'ig_type',
        'ig_user__project',
        'created_by_donor',
        'deleted_by_user',
        'ig_user',
    ]
    search_fields = [
        'ig_shortcode',
        'ig_id',
        'ig_user__ig_username',
    ]

    date_hierarchy = 'ig_taken_at_timestamp'


@admin.register(models.IgImage)
class IgImageAdmin(admin.ModelAdmin):
    list_display = [
        'ig_post',
        'image_url_link',
    ]
    exclude = ['image_url']
    readonly_fields = [
        'ig_post',
        'image_url_link',
    ]
    search_fields = ['ig_post__ig_shortcode']
    list_filter = [RacyFilter, 'ig_post__ig_type', 'ig_post__ig_user']
    date_hierarchy = 'ig_post__ig_taken_at_timestamp'

    def image_url_link(self, instance):
        return mark_safe(
            f'<a href="{instance.image_url}" target="_blank" rel="noopener noreferrer nofollow">{instance.image_url}</a>'
        )

    class GVisionAnalyseInlineAdmin(admin.StackedInline):
        model = models.GVisionAnalyse
        exclude = ['analyse']
        readonly_fields = ['analyse_prettified']

        def analyse_prettified(self, instance):
            """Function to display pretty version of our data"""
            # Convert the data to sorted, indented JSON
            response = json.dumps(instance.analyse, sort_keys=True, indent=2)
            # Get the Pygments formatter
            formatter = HtmlFormatter(style='colorful')
            # Highlight the data
            response = highlight(response, JsonLexer(), formatter)
            # Get the stylesheet
            style = "<style>" + formatter.get_style_defs() + "</style><br>"
            # Safe the output
            return mark_safe(style + response)

        analyse_prettified.short_description = 'analyse prettified'

    inlines = [GVisionAnalyseInlineAdmin]


@admin.register(models.IgUser)
class IgUserAdmin(admin.ModelAdmin):
    list_display = [
        'profile_pic',
        'ig_username',
        'ig_full_name',
        'ig_is_business_account',
        'ig_business_category_name',
        'is_active',
        'project',
        'last_scrape',
        'created_by',
        'created',
    ]

    search_fields = [
        'ig_username',
        'ig_full_name',
    ]

    def profile_pic(self, instance):
        if instance.ig_profile_pic:
            return mark_safe(
                f'<img width="50" src="{instance.ig_profile_pic.url}" /">')

    list_filter = [
        'project__name',
        'is_active',
        ('created_by', admin.RelatedOnlyFieldListFilter),
    ]

    readonly_fields = [
        'created_by',
    ]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Mark selected account as active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Mark selected account as inactive"

    actions = [make_active, make_inactive]
