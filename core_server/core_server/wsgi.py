"""
WSGI config for core_server project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_server.settings')

application = get_wsgi_application()

