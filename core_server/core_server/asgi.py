"""
ASGI config for core_server project.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_server.settings')

application = get_asgi_application()

