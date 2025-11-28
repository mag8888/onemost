# Исправление Root Directory для MLM сервера $100

## Вариант 1: Root Directory = корень проекта (РЕКОМЕНДУЕТСЯ)

### Настройка в Railway:

1. **Root Directory**: оставьте **пустым** (корень проекта)
2. **Start Command** (автоматически из railway.json):
   ```bash
   cd mlm_server && python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:${PORT:-8000}
   ```

### Преимущества:
- ✅ Модуль `shared` доступен напрямую
- ✅ Не нужно копировать файлы
- ✅ Проще управление

## Вариант 2: Root Directory = mlm_server

### Настройка в Railway:

1. **Root Directory**: `mlm_server`
2. **Start Command**:
   ```bash
   python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:${PORT:-8000}
   ```
3. **PYTHONPATH** (добавьте переменную окружения):
   ```env
   PYTHONPATH=/app/..:${PYTHONPATH}
   ```

### Преимущества:
- ✅ Изоляция сервера
- ✅ Чище структура

## Текущая конфигурация

В `railway.json` настроено для **Варианта 1** (Root Directory = корень):
- Start Command включает `cd mlm_server`

Если вы используете **Вариант 2** (Root Directory = mlm_server):
- Уберите `cd mlm_server` из Start Command
- Добавьте `PYTHONPATH=/app/..:${PYTHONPATH}` в переменные окружения

## Рекомендация

**Используйте Вариант 1** - Root Directory = корень проекта (пусто).

Это проще и надежнее.

