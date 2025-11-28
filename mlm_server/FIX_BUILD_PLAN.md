# Исправление ошибки "Error creating build plan with Railpack"

## Проблема

Ошибка: "Error creating build plan with Railpack" при сборке проекта в Railway.

## Причины

1. **Railway не может определить тип проекта** - нет явной конфигурации
2. **Root Directory установлен неправильно** - файлы не находятся
3. **Отсутствует nixpacks.toml** - Railway не знает, как собрать проект

## Решение

### Создан файл `nixpacks.toml`

Файл `nixpacks.toml` в директории `mlm_server/` явно указывает Railway, как собрать проект:

```toml
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = ["echo 'Build complete'"]

[start]
cmd = "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:${PORT:-8000}"
```

### Настройка Root Directory

**ВАЖНО:** Root Directory должен быть `mlm_server`!

1. В Railway откройте сервис MLM $100
2. Перейдите в **"Settings"** → **"Source"** (или **"Deploy"**)
3. Найдите **"Root Directory"**
4. Установите: **`mlm_server`**
5. Сохраните

### Проверка файлов

Убедитесь, что в `mlm_server/` есть:
- ✅ `requirements.txt`
- ✅ `manage.py`
- ✅ `nixpacks.toml` (новый файл)
- ✅ `railway.json`
- ✅ `mlm_server/settings.py`

## После исправления

1. Railway должен успешно определить тип проекта (Python/Django)
2. Сборка должна пройти успешно
3. Сервер должен запуститься

## Альтернатива

Если `nixpacks.toml` не помогает, можно использовать `railway.json` с явным указанием builder:

```json
{
  "build": {
    "builder": "NIXPACKS"
  }
}
```

Но `nixpacks.toml` более надежен для явной конфигурации.

