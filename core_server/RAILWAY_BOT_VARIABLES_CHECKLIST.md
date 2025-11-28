# Чеклист переменных для бота в Railway

## ✅ Уже есть (проверено на скриншоте):
- `SERVICE_TYPE=bot` ✅
- `TELEGRAM_BOT_TOKEN` ✅
- `MLM_SERVER_1_API_KEY` ✅
- `MLM_SERVER_20_API_KEY` ✅
- `SECRET_KEY` ✅
- `DEBUG` ✅
- `ALLOWED_HOSTS` ✅
- `DATABASE_PUBLIC_URL` ✅

## ❌ Нужно добавить/изменить:

### 1. DATABASE_URL (критично!)
**Действие:** Скопировать значение из `DATABASE_PUBLIC_URL` в новую переменную `DATABASE_URL`
- Или просто переименовать `DATABASE_PUBLIC_URL` → `DATABASE_URL`
- Код теперь поддерживает оба варианта, но лучше иметь `DATABASE_URL`

### 2. MLM_SERVER_1000_API_KEY (вместо MLM_SERVER_2_API_KEY)
**Действие:** 
- Удалить `MLM_SERVER_2_API_KEY`
- Добавить `MLM_SERVER_1000_API_KEY` (взять из переменных MLM сервера $1000)

### 3. MLM_PROGRAM_30_UPGRADE_URL
**Действие:** Добавить новую переменную
**Значение:** `https://your-mlm-server-30.railway.app/api/upgrade-partner/`
**Где взять:** Railway URL сервера $30 (ветка `3/20`) + `/api/upgrade-partner/`

### 4. MLM_PROGRAM_100_UPGRADE_URL
**Действие:** Добавить новую переменную
**Значение:** `https://your-mlm-server-100.railway.app/api/upgrade-partner/`
**Где взять:** Railway URL сервера $100 (ветка `3/100`) + `/api/upgrade-partner/`

### 5. MLM_PROGRAM_1000_UPGRADE_URL
**Действие:** Добавить новую переменную
**Значение:** `https://your-mlm-server-1000.railway.app/api/upgrade-partner/`
**Где взять:** Railway URL сервера $1000 (ветка `3/1000`) + `/api/upgrade-partner/`

## 📝 Пошаговая инструкция:

1. **Добавить DATABASE_URL:**
   - Откройте переменную `DATABASE_PUBLIC_URL`
   - Скопируйте её значение
   - Создайте новую переменную `DATABASE_URL` с тем же значением

2. **Заменить MLM_SERVER_2_API_KEY:**
   - Откройте MLM сервер $1000 в Railway
   - Скопируйте значение переменной `CORE_API_KEY` (или как она называется там)
   - В сервисе бота удалите `MLM_SERVER_2_API_KEY`
   - Добавьте `MLM_SERVER_1000_API_KEY` с скопированным значением

3. **Добавить URL для программы $30:**
   - Откройте MLM сервер $30 в Railway
   - Скопируйте его Railway URL (например, `mlm-server-30-production.up.railway.app`)
   - В сервисе бота добавьте переменную `MLM_PROGRAM_30_UPGRADE_URL`
   - Значение: `https://mlm-server-30-production.up.railway.app/api/upgrade-partner/`

4. **Добавить URL для программы $100:**
   - Откройте MLM сервер $100 в Railway
   - Скопируйте его Railway URL
   - В сервисе бота добавьте переменную `MLM_PROGRAM_100_UPGRADE_URL`
   - Значение: `https://your-mlm-server-100-url.railway.app/api/upgrade-partner/`

5. **Добавить URL для программы $1000:**
   - Откройте MLM сервер $1000 в Railway
   - Скопируйте его Railway URL
   - В сервисе бота добавьте переменную `MLM_PROGRAM_1000_UPGRADE_URL`
   - Значение: `https://your-mlm-server-1000-url.railway.app/api/upgrade-partner/`

## ✅ После добавления:

1. Перезапустите сервис бота в Railway
2. Проверьте логи - должны быть сообщения:
   - `Starting Telegram bot...`
   - `Bot is ready to receive messages`
   - НЕ должно быть ошибок о недостающих переменных
3. Проверьте бота в Telegram - отправьте `/start`

## 🔍 Как найти Railway URL MLM серверов:

1. Откройте проект в Railway
2. Найдите сервис MLM сервера (например, `mlm-server-30`)
3. Перейдите на вкладку **Settings**
4. Найдите раздел **Domains** или **Networking**
5. Там будет указан URL вида: `xxx-production.up.railway.app`
6. Добавьте к нему `/api/upgrade-partner/`

