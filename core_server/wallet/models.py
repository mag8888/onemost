"""
Модели кошелька и баланса
"""
from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Wallet(models.Model):
    """Кошелек пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet', verbose_name='Пользователь')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)], verbose_name='Баланс')
    total_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Всего заработано')
    total_withdrawn = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Всего выведено')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    
    class Meta:
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'
    
    def __str__(self):
        return f"Wallet {self.user.username} - {self.balance}"


class Transaction(models.Model):
    """Транзакции кошелька"""
    TRANSACTION_TYPES = [
        ('deposit', 'Пополнение'),
        ('withdrawal', 'Вывод'),
        ('bonus', 'Бонус'),
        ('referral_bonus', 'Реферальный бонус'),
        ('mlm_bonus', 'MLM бонус'),
        ('payment', 'Оплата'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('completed', 'Завершена'),
        ('failed', 'Ошибка'),
        ('cancelled', 'Отменена'),
    ]
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions', verbose_name='Кошелек')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, verbose_name='Тип')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    description = models.TextField(blank=True, verbose_name='Описание')
    mlm_server_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='MLM сервер')
    reference_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID ссылки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['wallet', 'created_at']),
            models.Index(fields=['transaction_type', 'status']),
        ]
    
    def __str__(self):
        return f"{self.wallet.user.username} - {self.amount} ({self.transaction_type})"


class WithdrawalRequest(models.Model):
    """Запросы на вывод средств"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('processing', 'Обрабатывается'),
        ('completed', 'Завершен'),
        ('rejected', 'Отклонен'),
    ]
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='withdrawal_requests', verbose_name='Кошелек')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Сумма')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    payment_method = models.CharField(max_length=50, verbose_name='Способ оплаты')
    payment_details = models.JSONField(default=dict, verbose_name='Детали оплаты')
    admin_notes = models.TextField(blank=True, verbose_name='Заметки администратора')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    
    class Meta:
        verbose_name = 'Запрос на вывод'
        verbose_name_plural = 'Запросы на вывод'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.wallet.user.username} - {self.amount} ({self.status})"

