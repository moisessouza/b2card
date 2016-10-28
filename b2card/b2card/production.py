from settings import *

DEBUG = True

SECRET_KEY = os.environ['OPENSHIFT_SECRET_TOKEN']

ALLOWED_HOSTS = [os.environ['OPENSHIFT_APP_DNS']]

STATIC_ROOT = os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', 'static')