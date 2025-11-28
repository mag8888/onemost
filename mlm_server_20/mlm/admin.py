"""
Админ-панель для MLM
"""
from django.contrib import admin
from .models import MLMNode, Bonus


@admin.register(MLMNode)
class MLMNodeAdmin(admin.ModelAdmin):
    """Админка для MLM узлов"""
    list_display = ['user_id', 'referrer_id', 'position', 'status', 'rank', 'partners_count', 'created_at']
    list_filter = ['status', 'rank', 'position', 'created_at']
    search_fields = ['user_id', 'referrer_id']


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    """Админка для бонусов"""
    list_display = ['user_id', 'referrer_id', 'bonus_type', 'amount', 'status', 'created_at']
    list_filter = ['bonus_type', 'status', 'created_at']
    search_fields = ['user_id', 'referrer_id']

