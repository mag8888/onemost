"""
URL configuration for mlm_server project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('mlm.urls')),
    path('api/', include('referrals.urls')),
]

