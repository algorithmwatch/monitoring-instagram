from google.cloud import vision
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToDict
from django.conf import settings

CREDENTIALS = service_account.Credentials.from_service_account_info(
    settings.GOOGLE_CLOUD_API_KEY)
CLIENT = vision.ImageAnnotatorClient(credentials=CREDENTIALS)


def analyse_image(image_url):
    response = CLIENT.annotate_image({
        'image': {
            # 'content': image_url
            'source': {
                'image_uri': image_url
            },
        },
        'features': [
            {
                'type': vision.enums.Feature.Type.TEXT_DETECTION
            },
            {
                'type': vision.enums.Feature.Type.LABEL_DETECTION
            },
            {
                'type': vision.enums.Feature.Type.SAFE_SEARCH_DETECTION
            },
        ],
    })
    if response.error.code != 0:
        raise GVisionException(
            f'Gvision  error with {image_url}: {response.error.message}')
    return MessageToDict(response)


class GVisionException(Exception):
    pass
