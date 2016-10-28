#!/usr/bin/python

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'b2card'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'b2card.production'

application = get_wsgi_application()