import os
from django.http import JsonResponse, HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from django.shortcuts import redirect

RELEASES = sorted(
    os.listdir(os.path.join(settings.BASE_DIR, 'static', 'web-ext-releases')))


def addon_updates_view(request):
    response = {
        'addons': {
            '{5afcda46-8767-438e-80ae-2c2c90482496}': {
                'updates': [{
                    'version': r.split('-')[1],
                    "update_link": get_release_absolute_url(r, request)
                } for r in RELEASES]
            }
        }
    }
    return JsonResponse(response)


def latest_firefox_view(request):
    if not RELEASES:
        return HttpResponse('Nothing')
    latest = get_release_absolute_url(RELEASES[-1], request)
    return redirect(latest)


def get_release_absolute_url(file_path, req):
    return req.build_absolute_uri(
        staticfiles_storage.url(f"web-ext-releases/{file_path}"))
