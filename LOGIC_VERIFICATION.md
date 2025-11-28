# Проверка логики MLM Server $20

## ✅ Логика реализована правильно

### При регистрации нового партнера (оплата $20):

1. **Пользователь платит $20** за статус партнера
2. **Реферер получает:**
   - **$10** - Желтый бонус
   - **$10** - Зеленый бонус
   - **Итого: $20**

### Код реализации

Файл: `mlm_server_20/mlm/services.py`

```python
def _calculate_yellow_and_green_bonuses(self, referrer_id: int, new_partner_id: int):
    """Рассчитать желтый и зеленый бонусы при регистрации нового партнера ($20)"""
    # Желтый бонус - $10 рефереру
    yellow_bonus = Bonus.objects.create(
        user_id=referrer_id,
        bonus_type='yellow',
        amount=Decimal(10.0),  # $10
        ...
    )
    
    # Зеленый бонус - $10 рефереру
    green_bonus = Bonus.objects.create(
        user_id=referrer_id,
        bonus_type='green',
        amount=Decimal(10.0),  # $10
        ...
    )
```

### Настройки

Файл: `mlm_server_20/mlm_server/settings.py`

```python
MLM_PARTNER_PRICE = 20.0    # Цена за партнера
MLM_YELLOW_BONUS = 10.0     # Желтый бонус
MLM_GREEN_BONUS = 10.0      # Зеленый бонус
```

### Модель бонусов

Файл: `mlm_server_20/mlm/models.py`

```python
BONUS_TYPES = [
    ('yellow', 'Желтый бонус'),      # ✅ Добавлен
    ('green', 'Зеленый бонус'),      # ✅ Добавлен
    ...
]
```

## ✅ Итог

- ✅ Желтый бонус $10 - реализован
- ✅ Зеленый бонус $10 - реализован
- ✅ Итого $20 рефереру - реализовано
- ✅ Логика вызывается при `upgrade_to_partner()`

**Логика работает корректно!**

