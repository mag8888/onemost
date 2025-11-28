"""
Telegram бот для центрального сервера
"""
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from django.conf import settings
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
        
        # Создаем или получаем пользователя
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
        try:
            user = User.objects.get(telegram_id=update.effective_user.id)
            mlm_server_id = context.args[0] if context.args else 'mlm_server_1'
            
            referral_link, _ = ReferralLink.objects.get_or_create(
                user=user,
                mlm_server_id=mlm_server_id
            )
            
            message = f"🔗 Ваша реферальная ссылка:\n{referral_link.referral_code}"
        except User.DoesNotExist:
            message = "Пользователь не найден. Используйте /start для регистрации."
        except Exception as e:
            message = f"Ошибка: {str(e)}"
        
        await update.message.reply_text(message)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'balance':
            try:
                user = User.objects.get(telegram_id=update.effective_user.id)
                wallet, _ = Wallet.objects.get_or_create(user=user)
                message = (
                    f"💰 Ваш баланс: {wallet.balance} руб.\n"
                    f"📈 Всего заработано: {wallet.total_earned} руб.\n"
                    f"💸 Всего выведено: {wallet.total_withdrawn} руб."
                )
            except User.DoesNotExist:
                message = "Пользователь не найден."
        
        elif query.data == 'referral':
            try:
                user = User.objects.get(telegram_id=update.effective_user.id)
                referral_link, _ = ReferralLink.objects.get_or_create(
                    user=user,
                    mlm_server_id='mlm_server_1'
                )
                message = f"🔗 Ваша реферальная ссылка:\n{referral_link.referral_code}"
            except User.DoesNotExist:
                message = "Пользователь не найден."
        
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
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
        except Exception as e:
            logger.error(f"Error running bot: {e}")
            raise


# Глобальный экземпляр бота
bot = TelegramBot()

