"""
Админ-панель для кошелька
"""
from django.contrib import admin
from .models import Wallet, Transaction, WithdrawalRequest


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """Админка для кошельков"""
    list_display = ['user', 'balance', 'total_earned', 'total_withdrawn', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Админка для транзакций"""
    list_display = ['wallet', 'amount', 'transaction_type', 'status', 'mlm_server_id', 'created_at']
    list_filter = ['transaction_type', 'status', 'mlm_server_id', 'created_at']
    search_fields = ['wallet__user__username', 'description', 'reference_id']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    """Админка для запросов на вывод"""
    list_display = ['wallet', 'amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['wallet__user__username', 'payment_details']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

