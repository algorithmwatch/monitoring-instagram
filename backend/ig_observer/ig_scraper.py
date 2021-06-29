import base64
import logging
import json
import pickle
import tempfile
import random
import time
from datetime import timedelta
import requests
from fake_headers import Headers
from django.db import transaction
from django.conf import settings
from django.core import files
from django.utils.timezone import datetime, make_aware, now
from ig_observer.models import IgPost

QUERY_HASH_GET_PROFILE = 'e769aa130647d2354c40ea6a439bfc08'
QUERY_HASH_GET_POST = '2b0673e0dc4580674a88d426fe00ea90'

logger = logging.getLogger(__name__)


def scrape_media(ig_user, keep_going=False):
    """ For every latest media for the given ig account, will save a Post.
    Stop when a media is already found in the DB """
    media = __fetch_media(ig_user.ig_id)
    if len(media['edges']) == 0:
        raise PrivateAccountException('This account seems to be private')
    continue_pagination = True
    total_created = 0
    total_existed = 0
    with transaction.atomic():
        while continue_pagination:
            for edge in media['edges']:
                node = edge['node']
                if node['owner']['username'] != ig_user.ig_username:
                    raise RenamedAccountException(
                        "IgUser %s has changed his name: %s" %
                        (ig_user.ig_username, node['owner']['username']))
                # check the post date and compare with a starting point
                timestamp = make_aware(
                    datetime.utcfromtimestamp(node['taken_at_timestamp']))
                if timestamp < (ig_user.created - timedelta(days=7)):
                    # will exit the while loop
                    continue_pagination = False
                    # exit the for loop
                    break
                post_instance, created = IgPost.objects.get_or_create_post(
                    node['id'], ig_user, node)
                if created:
                    total_created += 1
                # if already exists, we skip the rest, we already have them
                if not created and not post_instance.created_by_donor:
                    if keep_going:
                        total_existed += 1
                    else:
                        # will exit the while loop
                        continue_pagination = False
                        # exit the for loop
                        break
            if continue_pagination and media['has_next_page']:
                media = __fetch_media(ig_user.ig_id, media['end_cursor'])
            else:
                break
        # update last scrape date if everything was fine
        ig_user.last_scrape = now()
        ig_user.save()
    logger.info("Created %d (existed %d) posts for user %s", total_created,
                total_existed, ig_user)


def __get_shared_data(ig_username):
    headers = Headers(os="mac", headers=True).generate()
    res = requests.get(f"https://www.instagram.com/{ig_username}",
                       headers=headers,
                       timeout=3)
    shared_data = res.text.split("window._sharedData = ")[1].split(
        ";</script>")[0]
    shared_data = json.loads(shared_data)
    try:
        user = shared_data['entry_data']['ProfilePage'][0]['graphql']['user']
    except KeyError as error:
        logger.error('Error %s. code: %d.shared_data: %r', error,
                     res.status_code, shared_data)
        raise error
    return user


def __fetch_media(ig_id, cursor=''):
    """ Returns the 12 first media (after the given cursor) for the given ig profile. """
    variables = {
        "id": ig_id,
        "first": 12,
        "after": cursor,
    }
    data = __query_graphql(QUERY_HASH_GET_PROFILE, variables)
    edges = data['data']['user']['edge_owner_to_timeline_media']['edges']
    _page_info = data['data']['user']['edge_owner_to_timeline_media'][
        'page_info']
    has_next_page = _page_info['has_next_page']
    end_cursor = _page_info['end_cursor']
    return {
        'edges': edges,
        'has_next_page': has_next_page,
        'end_cursor': end_cursor,
    }


def get_or_complete_user_by_ig_username(ig_user):
    if not ig_user.ig_id:
        user_meta = __get_shared_data(ig_user.ig_username)
        ig_user.ig_id = user_meta['id']
        ig_user.ig_biography = user_meta['biography']
        ig_user.ig_business_category_name = user_meta['business_category_name']
        ig_user.ig_full_name = user_meta['full_name']
        ig_user.ig_profile_pic = __download_image(user_meta['profile_pic_url'])
        ig_user.ig_is_business_account = user_meta['is_business_account']
        ig_user.save()
    return ig_user


def __download_image(image_url):
    # Steam the image from the url
    req = requests.get(image_url, stream=True, timeout=3)
    # Was the request OK?
    req.raise_for_status()
    # Get the filename from the url, used for saving later
    file_name = image_url.split('/')[-1].split('?')[0]
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile()
    # Read the streamed image in sections
    for block in req.iter_content(1024 * 8):
        # If no more file then stop
        if not block:
            break
        # Write image block to temporary file
        temp_file.write(block)
    return files.File(temp_file, name=file_name)


def scrape_post(post_shortname):
    variables = {
        "shortcode": post_shortname,
        "child_comment_count": 3,
        "fetch_comment_count": 40,
        "parent_comment_count": 24,
        "has_threaded_comments": True
    }
    data = __query_graphql(QUERY_HASH_GET_POST, variables)
    return data['data']['shortcode_media']


def __query_graphql(query_hash, variables):
    time.sleep(random.randint(200, 600) / 100)
    headers = Headers(os="mac", headers=True).generate()
    cookies = pickle.loads(
        base64.decodebytes(settings.INSTAGRAM_SESSION_COOKIE.encode('utf8')))
    res = requests.get("https://www.instagram.com/graphql/query/?" +
                       f"query_hash={query_hash}" +
                       f"&variables={json.dumps(variables)}",
                       headers=headers,
                       timeout=3,
                       cookies=cookies)
    res.raise_for_status()
    data = res.json()
    return data


class RenamedAccountException(Exception):
    ...


class PrivateAccountException(Exception):
    ...
