import django_heroku
import os
from .settings import *

django_heroku.settings(locals())
SECRET_KEY = os.environ.get('SECRET_KEY')

# FIXME: check if addon update api and ig user avatar are working well
# STATIC_URL = "https://monitoring-ig.herokuapp.com/static/"

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_HSTS_SECONDS = 3600
# SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DEBUG = os.environ.get('DEBUG', 'false') == 'true'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'verbose': {
            'datefmt':
            '%Y-%m-%d %H:%M:%S',
            'format':
            '%(asctime)s [%(process)d] '
            '[%(levelname)s] pathname=%(pathname)s '
            'lineno=%(lineno)s funcname=%(funcName)s '
            '%(message)s'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
