"""
Telegram бот для центрального сервера
"""
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from telegram.error import Conflict, NetworkError, TimedOut
from django.conf import settings
from asgiref.sync import sync_to_async
from users.models import User
from wallet.models import Wallet
from users.models import ReferralLink

logger = logging.getLogger(__name__)


class TelegramBot:
    """Класс для управления Telegram ботом"""
    
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.application = None
    
    def setup(self):
        """Настройка бота"""
        logger.info(f"Setting up bot... Token exists: {bool(self.token)}")
        if not self.token:
            logger.error("TELEGRAM_BOT_TOKEN not set, bot will not start")
            logger.error("Please set TELEGRAM_BOT_TOKEN environment variable")
            return
        
        logger.info("Creating Telegram application...")
        self.application = Application.builder().token(self.token).build()
        
        # Добавляем обработчик ошибок
        async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
            """Обработчик ошибок"""
            logger.error(f"Exception while handling an update: {context.error}")
            if isinstance(context.error, Conflict):
                logger.error("=" * 50)
                logger.error("CRITICAL: CONFLICT detected!")
                logger.error("Another bot instance is running with the same token!")
                logger.error("=" * 50)
                logger.error("Please check:")
                logger.error("1. Other Railway services using the same token")
                logger.error("2. Old containers that didn't shut down")
                logger.error("3. Local bot instances")
                logger.error("4. Other Railway projects")
                logger.error("=" * 50)
                # Не пытаемся остановить бота - просто логируем и выходим
                import sys
                import os
                os._exit(1)  # Принудительный выход
        
        self.application.add_error_handler(error_handler)
        
        # Регистрация handlers
        logger.info("Registering command handlers...")
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("balance", self.balance_command))
        self.application.add_handler(CommandHandler("referral", self.referral_command))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        logger.info("Bot setup completed successfully")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        user = update.effective_user
        
        # Создаем или получаем пользователя (асинхронно)
        @sync_to_async
        def get_or_create_user():
            db_user, created = User.objects.get_or_create(
                telegram_id=user.id,
                defaults={
                    'username': user.username or f"user_{user.id}",
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            )
            if created:
                # Создаем кошелек
                Wallet.objects.create(user=db_user)
            return db_user, created
        
        db_user, created = await get_or_create_user()
        
        if created:
            message = f"Добро пожаловать, {user.first_name}! Вы успешно зарегистрированы."
        else:
            message = f"С возвращением, {user.first_name}!"
        
        keyboard = [
            [InlineKeyboardButton("💰 Баланс", callback_data='balance')],
            [InlineKeyboardButton("🔗 Реферальная ссылка", callback_data='referral')],
            [InlineKeyboardButton("📊 Статистика", callback_data='stats')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup)
    
    async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /balance"""
        try:
            user = User.objects.get(telegram_id=update.effective_user.id)
            wallet, _ = Wallet.objects.get_or_create(user=user)
            
            message = (
                f"💰 Ваш баланс: {wallet.balance} руб.\n"
                f"📈 Всего заработано: {wallet.total_earned} руб.\n"
                f"💸 Всего выведено: {wallet.total_withdrawn} руб."
            )
        except User.DoesNotExist:
            message = "Пользователь не найден. Используйте /start для регистрации."
        
        await update.message.reply_text(message)
    
    async def referral_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /referral"""
        mlm_server_id = context.args[0] if context.args else 'mlm_server_1'
        
        @sync_to_async
        def get_referral_link():
            try:
                user = User.objects.get(telegram_id=update.effective_user.id)
                referral_link, _ = ReferralLink.objects.get_or_create(
                    user=user,
                    mlm_server_id=mlm_server_id
                )
                return f"🔗 Ваша реферальная ссылка:\n{referral_link.referral_code}"
            except User.DoesNotExist:
                return "Пользователь не найден. Используйте /start для регистрации."
            except Exception as e:
                return f"Ошибка: {str(e)}"
        
        message = await get_referral_link()
        await update.message.reply_text(message)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'balance':
            @sync_to_async
            def get_balance():
                try:
                    user = User.objects.get(telegram_id=update.effective_user.id)
                    wallet, _ = Wallet.objects.get_or_create(user=user)
                    return (
                        f"💰 Ваш баланс: {wallet.balance} руб.\n"
                        f"📈 Всего заработано: {wallet.total_earned} руб.\n"
                        f"💸 Всего выведено: {wallet.total_withdrawn} руб."
                    )
                except User.DoesNotExist:
                    return "Пользователь не найден."
            
            message = await get_balance()
        
        elif query.data == 'referral':
            @sync_to_async
            def get_referral_link():
                try:
                    user = User.objects.get(telegram_id=update.effective_user.id)
                    referral_link, _ = ReferralLink.objects.get_or_create(
                        user=user,
                        mlm_server_id='mlm_server_1'
                    )
                    return f"🔗 Ваша реферальная ссылка:\n{referral_link.referral_code}"
                except User.DoesNotExist:
                    return "Пользователь не найден."
            
            message = await get_referral_link()
        
        else:
            message = "Функция в разработке."
        
        await query.edit_message_text(message)
    
    def run(self):
        """Запуск бота"""
        if not self.application:
            logger.error("Bot not setup, cannot run")
            logger.error("Check if TELEGRAM_BOT_TOKEN is set in environment variables")
            return
        
        logger.info("=" * 50)
        logger.info("Starting Telegram bot...")
        logger.info("Bot is ready to receive messages")
        logger.info("=" * 50)
        
        try:
            # Инициализируем бота перед polling
            async def post_init(app: Application) -> None:
                """Выполняется после инициализации"""
                logger.info("Bot initialized successfully")
            
            async def post_shutdown(app: Application) -> None:
                """Выполняется при остановке"""
                logger.info("Bot is shutting down...")
            
            self.application.post_init = post_init
            self.application.post_shutdown = post_shutdown
            
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                close_loop=False
            )
        except Conflict as e:
            logger.error("=" * 50)
            logger.error("CRITICAL: CONFLICT detected during startup!")
            logger.error("Another bot instance is running with the same token!")
            logger.error(f"Error: {e}")
            logger.error("=" * 50)
            logger.error("SOLUTION:")
            logger.error("1. Check ALL Railway services - stop any other bot instances")
            logger.error("2. Check ALL Railway projects - ensure no duplicate bots")
            logger.error("3. Wait 2-3 minutes after stopping other instances")
            logger.error("4. Restart this service")
            logger.error("=" * 50)
            # Принудительный выход
            import sys
            import os
            os._exit(1)
        except (NetworkError, TimedOut) as e:
            logger.warning(f"Network error: {e}. Retrying in 30 seconds...")
            import time
            time.sleep(30)
            self.run()
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Error running bot: {e}")
            logger.error("Bot will retry in 60 seconds...")
            import time
            time.sleep(60)
            self.run()


# Глобальный экземпляр бота
bot = TelegramBot()

