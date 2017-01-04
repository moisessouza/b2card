#!/usr/bin/python

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'b2card.local'

application = get_wsgi_application()