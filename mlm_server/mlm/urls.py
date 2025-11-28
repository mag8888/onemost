"""
URLs для MLM API
"""
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('upgrade-partner/', views.upgrade_to_partner, name='upgrade_to_partner'),
    path('check-rank/', views.check_rank_upgrade, name='check_rank_upgrade'),
]

