"""
URLs для веб-интерфейса
"""
from django.urls import path
from django.views.generic import TemplateView

from .views import StructureView

urlpatterns = [
    path('', TemplateView.as_view(template_name='web/index.html'), name='index'),
    path('dashboard/', TemplateView.as_view(template_name='web/dashboard.html'), name='dashboard'),
    path('structures/', StructureView.as_view(), name='structures'),
]

