"""
Модели пользователей
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Расширенная модель пользователя"""
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True, verbose_name='Telegram ID')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    is_partner = models.BooleanField(default=False, verbose_name='Партнер')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    
    # MLM статусы по серверам
    mlm_statuses = models.JSONField(default=dict, blank=True, verbose_name='MLM статусы')
    mlm_ranks = models.JSONField(default=dict, blank=True, verbose_name='MLM ранги')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username or f"User {self.id}"


class ReferralLink(models.Model):
    """Реферальные ссылки пользователей"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_links', verbose_name='Пользователь')
    mlm_server_id = models.CharField(max_length=100, verbose_name='MLM сервер')
    referral_code = models.CharField(max_length=50, unique=True, verbose_name='Реферальный код')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    
    class Meta:
        verbose_name = 'Реферальная ссылка'
        verbose_name_plural = 'Реферальные ссылки'
        unique_together = ['user', 'mlm_server_id']
    
    def __str__(self):
        return f"{self.user.username} - {self.mlm_server_id}"


class ReferralRelation(models.Model):
    """Реферальные связи между пользователями"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals', verbose_name='Пользователь')
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_made', verbose_name='Реферер')
    mlm_server_id = models.CharField(max_length=100, verbose_name='MLM сервер')
    level = models.IntegerField(default=1, verbose_name='Уровень')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    
    class Meta:
        verbose_name = 'Реферальная связь'
        verbose_name_plural = 'Реферальные связи'
        unique_together = ['user', 'mlm_server_id']
        indexes = [
            models.Index(fields=['referrer', 'mlm_server_id']),
            models.Index(fields=['user', 'mlm_server_id']),
        ]
    
    def __str__(self):
        return f"{self.referrer.username} -> {self.user.username} ({self.mlm_server_id})"

