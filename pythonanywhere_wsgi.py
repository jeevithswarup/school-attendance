# ============================================================
# PASTE THIS ENTIRE FILE into your PythonAnywhere WSGI config
# Replace YOUR_USERNAME with your actual PythonAnywhere username
# ============================================================

import sys
import os

# Path to your project
path = '/home/YOUR_USERNAME/school-attendance'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
