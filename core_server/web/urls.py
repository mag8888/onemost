"""
URLs для веб-интерфейса
"""
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='web/index.html'), name='index'),
    path('dashboard/', TemplateView.as_view(template_name='web/dashboard.html'), name='dashboard'),
]

