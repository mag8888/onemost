# Инструкции по развертыванию

## 📋 Быстрая инструкция

### 1. Загрузка в GitHub

```bash
# Перейдите в директорию проекта
cd /Users/ADMIN/onemost

# Запустите скрипт автоматической загрузки
./deploy_to_github.sh
```

Или выполните вручную (см. `GIT_DEPLOY.md`):

```bash
# Core Server → ветка centr
git checkout -b centr
git add core_server/ shared/ .gitignore README.md QUICKSTART.md RAILWAY_SETUP.md
git commit -m "Core Server"
git push -u origin centr

# MLM Server $100 → ветка 3/100
git checkout -b 3/100
git add mlm_server/ shared/
git commit -m "MLM Server $100"
git push -u origin 3/100

# MLM Server $20 → ветка 3/20
git checkout -b 3/20
git add mlm_server_20/ shared/
git commit -m "MLM Server $20"
git push -u origin 3/20
```

### 2. Деплой на Railway

Следуйте подробной инструкции в файле **`RAILWAY_SETUP.md`**

#### Краткая версия:

1. **Создайте проект на Railway**
   - Зайдите на [railway.app](https://railway.app)
   - Создайте новый проект
   - Подключите GitHub репозиторий

2. **Разверните Core Server**
   - Новый сервис → GitHub Repo
   - Ветка: `centr`
   - Root Directory: `core_server`
   - Добавьте PostgreSQL базу данных
   - Настройте переменные окружения (см. `RAILWAY_SETUP.md`)

3. **Разверните Telegram бота**
   - Новый сервис → GitHub Repo
   - Ветка: `centr`
   - Root Directory: `core_server`
   - Start Command: `python manage.py run_telegram_bot`

4. **Разверните MLM Server $100**
   - Новый сервис → GitHub Repo
   - Ветка: `3/100`
   - Root Directory: `mlm_server`
   - Настройте переменные окружения

5. **Разверните MLM Server $20**
   - Новый сервис → GitHub Repo
   - Ветка: `3/20`
   - Root Directory: `mlm_server_20`
   - Настройте переменные окружения

## 🔑 Важные переменные окружения

### Core Server

```env
SECRET_KEY=<сгенерируйте>
TELEGRAM_BOT_TOKEN=<от @BotFather>
MLM_SERVER_1_API_KEY=<случайная строка>
MLM_SERVER_2_API_KEY=<случайная строка>
MLM_SERVER_20_API_KEY=<случайная строка>
```

### MLM Server $100

```env
CORE_API_URL=https://your-core.railway.app/api
CORE_API_KEY=<тот же, что MLM_SERVER_1_API_KEY>
SERVER_ID=mlm_server_1
```

### MLM Server $20

```env
CORE_API_URL=https://your-core.railway.app/api
CORE_API_KEY=<тот же, что MLM_SERVER_20_API_KEY>
SERVER_ID=mlm_server_20
```

## ✅ Чеклист

- [ ] Код загружен в GitHub (ветки: centr, 3/100, 3/20)
- [ ] Создан проект на Railway
- [ ] Развернут Core Server
- [ ] Добавлена PostgreSQL база данных
- [ ] Настроены переменные окружения
- [ ] Запущен Telegram бот
- [ ] Развернут MLM Server $100
- [ ] Развернут MLM Server $20
- [ ] Проверена работа всех сервисов

## 📚 Дополнительная документация

- `RAILWAY_SETUP.md` - подробная инструкция по Railway
- `GIT_DEPLOY.md` - инструкция по загрузке в GitHub
- `docs/railway_deployment.md` - детальная документация
- `docs/architecture.md` - архитектура системы
- `docs/api.md` - API документация

## 🆘 Проблемы?

1. Проверьте логи в Railway Dashboard
2. Убедитесь, что все переменные окружения установлены
3. Проверьте, что код в правильных ветках
4. См. раздел "Решение проблем" в `RAILWAY_SETUP.md`

