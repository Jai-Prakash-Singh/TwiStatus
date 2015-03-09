"""
Django settings for twitter_status project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%ru!_qp73gr)ytfwntjlsmi0-#fo2)o20n&$_wl_!&_ex5kj@&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'status_reply',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'twitter_status.urls'

WSGI_APPLICATION = 'twitter_status.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

CONSUMER_KEY = 'bsjANsQfkTDfLQqyAPEdQb5tE'
CONSUMER_SECRET = 'VKGAWEiQXvgqA8kqjG5w7bEVAWTSZd2MjevV2wilsNzBmm76R8'
ACCESS_TOKEN = '519973818-WwH5f7XfUSlIftoHkLpoj7F8j8AgYnRc9BPCd4cR'
ACCESSTOKEN_SECRET = 'dpKnEDbMg2Wxhsue1sdJJZkvHQDlsXtxZ50JvHGlcUQij'

#import twitter
import tweepy
#TWITTER_API = twitter.Api(consumer_key=CONSUMER_KEY,
#                consumer_secret=CONSUMER_SECRET,
#                access_token_key=ACCESS_TOKEN,
#                access_token_secret=ACCESSTOKEN_SECRET)


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESSTOKEN_SECRET)
TWITTER_API = tweepy.API(auth)


from requests_oauthlib import OAuth1Session
request_twitter_api = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=ACCESS_TOKEN, resource_owner_secret=ACCESSTOKEN_SECRET)
