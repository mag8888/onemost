"""
Админ-панель для пользователей
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ReferralLink, ReferralRelation


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админка для пользователей"""
    list_display = ['id', 'username', 'telegram_id', 'email', 'is_partner', 'is_active', 'created_at']
    list_filter = ['is_partner', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'telegram_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительно', {
            'fields': ('telegram_id', 'phone', 'is_partner', 'mlm_statuses', 'mlm_ranks')
        }),
    )


@admin.register(ReferralLink)
class ReferralLinkAdmin(admin.ModelAdmin):
    """Админка для реферальных ссылок"""
    list_display = ['user', 'mlm_server_id', 'referral_code', 'created_at']
    list_filter = ['mlm_server_id', 'created_at']
    search_fields = ['user__username', 'referral_code']


@admin.register(ReferralRelation)
class ReferralRelationAdmin(admin.ModelAdmin):
    """Админка для реферальных связей"""
    list_display = ['referrer', 'user', 'mlm_server_id', 'level', 'created_at']
    list_filter = ['mlm_server_id', 'level', 'created_at']
    search_fields = ['referrer__username', 'user__username']

