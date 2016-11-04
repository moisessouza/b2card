from settings import *

DEBUG = True

SECRET_KEY = os.environ['OPENSHIFT_SECRET_TOKEN']

ALLOWED_HOSTS = [os.environ['OPENSHIFT_APP_DNS']]

STATIC_ROOT = os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'b2card',
        'USER': 'adminzWjjlwQ',
        'PASSWORD': '5G6qqBp2z5Tp',
        'HOST': os.environ['OPENSHIFT_MYSQL_DB_HOST'],   # Or an IP Address that your DB is hosted on
        'PORT': os.environ['OPENSHIFT_MYSQL_DB_PORT'],
    }
}