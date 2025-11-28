"""
Telegram бот для центрального сервера
"""
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from telegram.error import TelegramError
from django.conf import settings
from asgiref.sync import sync_to_async
from users.models import User
from wallet.models import Wallet
from users.models import ReferralLink, ReferralRelation

logger = logging.getLogger(__name__)


class TelegramBot:
    """Класс для управления Telegram ботом"""
    
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.application = None
    
    def setup(self):
        """Настройка бота"""
        if not self.token:
            logger.warning("TELEGRAM_BOT_TOKEN not set, bot will not start")
            return
        
        self.application = Application.builder().token(self.token).build()
        
        # Регистрация handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("balance", self.balance_command))
        self.application.add_handler(CommandHandler("referral", self.referral_command))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        user = update.effective_user
        referrer_user = None
        
        # Обработка реферальной ссылки (если есть параметр start)
        if context.args and len(context.args) > 0:
            referrer_identifier = context.args[0]
            logger.info(f"User {user.id} came from referral: {referrer_identifier}")
            
            # Ищем реферера по username или telegram_id
            @sync_to_async
            def find_referrer():
                referrer = None
                # Пытаемся найти по telegram_id (если передан ID)
                if referrer_identifier.isdigit():
                    try:
                        referrer = User.objects.get(telegram_id=int(referrer_identifier))
                    except User.DoesNotExist:
                        pass
                else:
                    # Ищем по username
                    try:
                        referrer = User.objects.get(username=referrer_identifier)
                    except User.DoesNotExist:
                        # Если не найден по username, пробуем найти по telegram_id из username
                        pass
                return referrer
            
            referrer_user = await find_referrer()
        
        # Создаем или получаем пользователя
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
        
        # Создаем реферальную связь, если есть реферер
        if referrer_user and referrer_user.id != db_user.id:
            @sync_to_async
            def create_referral_relation():
                # Создаем реферальную связь для всех MLM серверов
                for mlm_server_id in ['mlm_server_1', 'mlm_server_20']:
                    ReferralRelation.objects.get_or_create(
                        user=db_user,
                        referrer=referrer_user,
                        mlm_server_id=mlm_server_id,
                        defaults={'level': 1}
                    )
                logger.info(f"Referral relation created: {db_user.username} referred by {referrer_user.username}")
            
            await create_referral_relation()
            
            # Отправляем поздравление рефереру
            @sync_to_async
            def send_congratulations():
                try:
                    # Формируем информацию о новом пользователе
                    new_user_info = user.username if user.username else f"{user.first_name or ''} {user.last_name or ''}".strip() or f"ID: {user.id}"
                    
                    congratulation_message = (
                        f"🎉 Поздравляю!\n\n"
                        f"По вашей ссылке подключился: {new_user_info}"
                    )
                    
                    # Отправляем сообщение рефереру
                    return referrer_user.telegram_id, congratulation_message
                except Exception as e:
                    logger.error(f"Error preparing congratulations: {e}")
                    return None, None
            
            referrer_telegram_id, congratulation_message = await send_congratulations()
            
            if referrer_telegram_id and congratulation_message:
                try:
                    await context.bot.send_message(
                        chat_id=referrer_telegram_id,
                        text=congratulation_message
                    )
                    logger.info(f"Congratulations sent to referrer {referrer_telegram_id}")
                except TelegramError as e:
                    logger.error(f"Error sending congratulations to referrer {referrer_telegram_id}: {e}")
        
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
            return
        
        logger.info("Starting Telegram bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


# Глобальный экземпляр бота
bot = TelegramBot()

