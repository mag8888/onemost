"""
Модели MLM системы (локальная структура)
"""
from django.db import models
from django.conf import settings


class MLMNode(models.Model):
    """Узел MLM структуры (локальное представление)"""
    user_id = models.BigIntegerField(verbose_name='ID пользователя в Core')
    referrer_id = models.BigIntegerField(null=True, blank=True, verbose_name='ID реферера')
    position = models.CharField(max_length=10, choices=[('left', 'Слева'), ('center', 'Центр'), ('right', 'Справа')], default='left', verbose_name='Позиция')
    status = models.CharField(max_length=20, default='participant', verbose_name='Статус')  # participant, partner
    rank = models.CharField(max_length=20, default='0', verbose_name='Ранг')  # 0, ПУ1, ПУ2, ...
    partners_count = models.IntegerField(default=0, verbose_name='Количество партнеров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    
    class Meta:
        verbose_name = 'MLM узел'
        verbose_name_plural = 'MLM узлы'
        unique_together = ['user_id', 'referrer_id']
        indexes = [
            models.Index(fields=['referrer_id', 'position']),
            models.Index(fields=['user_id']),
        ]
    
    def __str__(self):
        return f"Node {self.user_id} (Status: {self.status}, Rank: {self.rank})"


class Bonus(models.Model):
    """Бонусы MLM системы"""
    BONUS_TYPES = [
        ('green_1', 'Зеленый бонус (1-й партнер)'),
        ('green_2', 'Зеленый бонус (2-й партнер)'),
        ('red', 'Красный бонус'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('sent', 'Отправлен'),
        ('failed', 'Ошибка'),
    ]
    
    user_id = models.BigIntegerField(verbose_name='ID пользователя')
    referrer_id = models.BigIntegerField(verbose_name='ID реферера')
    bonus_type = models.CharField(max_length=20, choices=BONUS_TYPES, verbose_name='Тип бонуса')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    
    class Meta:
        verbose_name = 'Бонус'
        verbose_name_plural = 'Бонусы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Bonus {self.bonus_type} - {self.amount} (User: {self.user_id})"

