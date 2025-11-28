"""
URLs для реферальной системы
"""
from django.urls import path
from . import views

urlpatterns = [
    path('get-structure/', views.get_structure, name='get_structure'),
]

