import hashlib
import base64
from django.conf import settings


def get_anonymous_id_from_username(username):
    return base64.urlsafe_b64encode(
        hashlib.pbkdf2_hmac('md5', username.encode(),
                            settings.IG_USERNAME_SALT_SECRET_KEY.encode(),
                            100000).hex().encode()).decode()
