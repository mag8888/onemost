"""
Расширенный Telegram-бот с каталогом программ и пополнением баланса.
"""
import asyncio
import logging
from decimal import Decimal, InvalidOperation

import requests
from asgiref.sync import sync_to_async
from django.conf import settings
from django.utils import timezone
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from users.models import User, ReferralLink, ReferralRelation
from wallet.models import Wallet, Transaction

logger = logging.getLogger(__name__)


PROGRAMS = {
    '30': {
        'title': 'Программа $30',
        'price': Decimal('30'),
        'mlm_server_id': 'mlm_server_20',
        'upgrade_url': settings.MLM_PROGRAM_30_UPGRADE_URL,
        'description': settings.MLM_PROGRAM_30_DESCRIPTION,
    },
    '100': {
        'title': 'Программа $100',
        'price': Decimal('100'),
        'mlm_server_id': 'mlm_server_1',
        'upgrade_url': settings.MLM_PROGRAM_100_UPGRADE_URL,
        'description': settings.MLM_PROGRAM_100_DESCRIPTION,
    },
    '1000': {
        'title': 'Программа $1000',
        'price': Decimal('1000'),
        'mlm_server_id': 'mlm_server_1000',
        'upgrade_url': settings.MLM_PROGRAM_1000_UPGRADE_URL,
        'description': settings.MLM_PROGRAM_1000_DESCRIPTION,
    },
}

MENU_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("💰 Баланс"), KeyboardButton("📋 Каталог программ")],
        [KeyboardButton("🔗 Реф программа")],
    ],
    resize_keyboard=True,
)


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
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message)
        )
        
        # Глобальный обработчик ошибок
        self.application.add_error_handler(self.error_handler)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        try:
            logger.info(f"Received /start command from user {update.effective_user.id}")
            
            # Получаем параметры команды (для реферальных ссылок)
            args = context.args
            referrer_username = args[0] if args else None
            
            # Создаём или получаем пользователя
            user = await self._get_or_create_user(update.effective_user)
            logger.info(f"User {user.id} created/retrieved successfully")
            
            # Обработка реферальной ссылки
            if referrer_username and referrer_username.strip():
                try:
                    await self._handle_referral(user, referrer_username)
                except Exception as ref_error:
                    logger.error(f"Error processing referral link: {ref_error}", exc_info=True)
            
            message = (
                f"Добро пожаловать, {user.first_name or user.username}!\n\n"
                "Используйте кнопки меню, чтобы пополнить баланс, посмотреть каталог программ "
                "и получить реферальную ссылку."
            )

            # Проверяем наличие update.message
            if update.message:
                await update.message.reply_text(message, reply_markup=MENU_KEYBOARD)
            elif update.effective_message:
                await update.effective_message.reply_text(message, reply_markup=MENU_KEYBOARD)
            else:
                logger.error("No message or effective_message in update")
                return
                
            logger.info(f"Welcome message sent to user {user.id}")
        except Exception as e:
            logger.error(f"Error in start_command: {e}", exc_info=True)
            try:
                if update.message:
                    await update.message.reply_text(
                        "Произошла ошибка при обработке команды. Попробуйте позже."
                    )
                elif update.effective_message:
                    await update.effective_message.reply_text(
                        "Произошла ошибка при обработке команды. Попробуйте позже."
                    )
            except Exception as send_error:
                logger.error(f"Error sending error message: {send_error}")

    async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /balance"""
        await self._send_balance_info(update, context)

    async def referral_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /referral"""
        await self._send_referral_link(update, context)

    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений (reply-клавиатура)"""
        text = (update.message.text or "").strip()

        # Проверка режима пополнения
        if context.user_data.get('awaiting_topup'):
            await self._handle_topup_amount(update, context, text)
            return

        if text == "💰 Баланс":
            await self._send_balance_info(update, context)
        elif text == "📋 Каталог программ":
            await self._show_program_catalog(update)
        elif text == "🔗 Реф программа":
            await self._send_referral_link(update, context)
        else:
            await update.message.reply_text(
                "Используйте кнопки меню или /start, чтобы увидеть доступные действия.",
                reply_markup=MENU_KEYBOARD,
            )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка нажатий на inline-кнопки"""
        query = update.callback_query
        await query.answer()
        data = query.data

        if data == 'topup':
            context.user_data['awaiting_topup'] = True
            await query.message.reply_text(
                "Введите сумму пополнения (например, 35.5). Отправьте 'отмена' для выхода.",
                reply_markup=MENU_KEYBOARD,
            )
            return

        if data.startswith('program_select_'):
            program_key = data.split('_', 2)[2]
            await self._send_program_details(query, program_key)
            return

        if data.startswith('program_info_'):
            program_key = data.split('_', 2)[2]
            program = PROGRAMS.get(program_key)
            if not program:
                await query.message.reply_text("Программа не найдена.")
                return
            await query.message.reply_text(program['description'])
            return

        if data.startswith('program_pay_'):
            program_key = data.split('_', 2)[2]
            await self._handle_program_payment(query, context, program_key)
            return

        await query.message.reply_text("Функция в разработке.")

    async def _send_balance_info(self, update_or_query, context):
        user = await self._get_or_create_user(update_or_query.effective_user)
        wallet = await self._get_wallet(user)
        text = (
            f"💰 Баланс: {wallet.balance} USD\n"
            f"📈 Всего заработано: {wallet.total_earned} USD\n"
            f"💸 Всего списано: {wallet.total_withdrawn} USD"
        )
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("➕ Пополнить баланс", callback_data='topup')]]
        )

        if getattr(update_or_query, "callback_query", None):
            await update_or_query.callback_query.message.reply_text(text, reply_markup=keyboard)
        else:
            await update_or_query.message.reply_text(text, reply_markup=keyboard)

    async def _send_referral_link(self, update_or_query, context):
        user = await self._get_or_create_user(update_or_query.effective_user)

        def _get_link():
            link, _ = ReferralLink.objects.get_or_create(
                user=user,
                mlm_server_id='mlm_server_unified',
                defaults={'referral_code': user.username or str(user.telegram_id)},
            )
            username = update_or_query.effective_user.username or str(user.telegram_id)
            return f"https://t.me/onemost_bot?start={username}"

        bot_link = await sync_to_async(_get_link)()
        text = (
            "🔗 Ваша единая реферальная ссылка:\n\n"
            f"{bot_link}\n\n"
            "Ссылка подходит для всех программ ($30, $100 и $1000)."
        )

        target = (
            update_or_query.callback_query.message
            if getattr(update_or_query, "callback_query", None)
            else update_or_query.message
        )
        await target.reply_text(text, reply_markup=MENU_KEYBOARD)

    async def _show_program_catalog(self, update_or_query):
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("💵 Программа $30", callback_data='program_select_30')],
                [InlineKeyboardButton("💵 Программа $100", callback_data='program_select_100')],
                [InlineKeyboardButton("💵 Программа $1000", callback_data='program_select_1000')],
            ]
        )
        target = (
            update_or_query.callback_query.message
            if getattr(update_or_query, "callback_query", None)
            else update_or_query.message
        )
        await target.reply_text("📋 Выберите реферальную программу:", reply_markup=keyboard)

    async def _send_program_details(self, query, program_key: str):
        program = PROGRAMS.get(program_key)
        if not program:
            await query.message.reply_text("Программа не найдена.")
            return

        text = (
            f"{program['title']}\n"
            f"Стоимость: ${program['price']}\n\n"
            "Нажмите «ℹ️ О продукте», чтобы узнать подробности, или «💳 Оплатить» "
            "для активации тарифа."
        )
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ℹ️ О продукте", callback_data=f'program_info_{program_key}')],
                [InlineKeyboardButton("💳 Оплатить", callback_data=f'program_pay_{program_key}')],
            ]
        )
        await query.message.reply_text(text, reply_markup=keyboard)

    async def _handle_topup_amount(self, update, context, text: str):
        if text.lower() in {'cancel', 'отмена'}:
            context.user_data['awaiting_topup'] = False
            await update.message.reply_text("Пополнение отменено.", reply_markup=MENU_KEYBOARD)
            return

        try:
            amount = Decimal(text.replace(',', '.'))
            if amount <= 0:
                raise InvalidOperation
        except (InvalidOperation, ValueError):
            await update.message.reply_text(
                "Введите положительное число. Пример: 25 или 49.9. Для отмены напишите 'отмена'."
            )
            return

        user = await self._get_or_create_user(update.effective_user)
        wallet = await self._change_balance(user, amount, 'deposit', 'Пополнение через Telegram бота')
        context.user_data['awaiting_topup'] = False

        await update.message.reply_text(
            f"✅ Баланс пополнен на ${amount}. Текущий баланс: ${wallet.balance}.",
            reply_markup=MENU_KEYBOARD,
        )

    async def _handle_program_payment(self, query, context, program_key: str):
        program = PROGRAMS.get(program_key)
        if not program:
            await query.message.reply_text("Программа не найдена.")
            return

        user = await self._get_or_create_user(query.from_user)
        wallet = await self._get_wallet(user)

        price = program['price']
        if wallet.balance < price:
            need = price - wallet.balance
            await query.message.reply_text(
                f"Недостаточно средств. Необходимо пополнить ещё ${need:.2f}.",
                reply_markup=MENU_KEYBOARD,
            )
            return

        wallet = await self._change_balance(
            user,
            -price,
            'payment',
            f'Покупка {program["title"]}',
        )
        await self._store_program_purchase(user, program_key)

        await query.message.reply_text(
            f"✅ {program['title']} оплачена. Ваш текущий баланс: ${wallet.balance:.2f}.\n"
            "Начисляем бонусы и обновляем статус партнёра...",
            reply_markup=MENU_KEYBOARD,
        )

        await self._notify_mlm_server(program_key, user.id)

    @staticmethod
    @sync_to_async
    def _get_or_create_user(tg_user):
        user, created = User.objects.get_or_create(
            telegram_id=tg_user.id,
            defaults={
                'username': tg_user.username or f"user_{tg_user.id}",
                'first_name': tg_user.first_name,
                'last_name': tg_user.last_name,
            },
        )
        if created:
            Wallet.objects.create(user=user)
        return user

    @staticmethod
    @sync_to_async
    def _get_wallet(user):
        wallet, _ = Wallet.objects.get_or_create(user=user)
        return wallet

    @staticmethod
    @sync_to_async
    def _handle_referral(user, referrer_username: str):
        """Обработка реферальной ссылки при регистрации"""
        if not referrer_username or not isinstance(referrer_username, str):
            logger.warning(f"Invalid referrer_username: {referrer_username}")
            return
        
        try:
            # Ищем реферера по username или telegram_id
            referrer = None
            referrer_username_clean = referrer_username.strip()
            
            if referrer_username_clean.isdigit():
                # Если это число, ищем по telegram_id
                try:
                    referrer = User.objects.filter(telegram_id=int(referrer_username_clean)).first()
                except (ValueError, TypeError):
                    logger.warning(f"Invalid telegram_id format: {referrer_username_clean}")
            else:
                # Ищем по username
                referrer = User.objects.filter(username=referrer_username_clean).first()
            
            if not referrer:
                logger.warning(f"Referrer not found: {referrer_username_clean}")
                return
            
            # Создаём реферальную связь для всех MLM серверов
            # (пока создаём для всех, потом можно будет выбрать конкретный)
            mlm_servers = ['mlm_server_1', 'mlm_server_20', 'mlm_server_1000']
            for mlm_server_id in mlm_servers:
                ReferralRelation.objects.get_or_create(
                    user=user,
                    mlm_server_id=mlm_server_id,
                    defaults={'referrer': referrer, 'level': 1}
                )
            
            logger.info(f"Referral relation created: {referrer.username or referrer.id} -> {user.username or user.id}")
        except Exception as e:
            logger.error(f"Error handling referral: {e}", exc_info=True)

    @staticmethod
    @sync_to_async
    def _change_balance(user, amount: Decimal, transaction_type: str, description: str):
        wallet, _ = Wallet.objects.get_or_create(user=user)
        wallet.balance = wallet.balance + amount
        wallet.save(update_fields=['balance', 'updated_at'])

        Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type=transaction_type,
            status='completed',
            description=description,
            mlm_server_id='core',
        )
        return wallet

    @staticmethod
    @sync_to_async
    def _store_program_purchase(user, program_key: str):
        statuses = user.mlm_statuses or {}
        programs = statuses.get('programs', {})
        programs[program_key] = {
            'title': PROGRAMS[program_key]['title'],
            'price': str(PROGRAMS[program_key]['price']),
            'purchased_at': timezone.now().isoformat(),
        }
        statuses['programs'] = programs
        user.mlm_statuses = statuses
        user.save(update_fields=['mlm_statuses'])

    async def _notify_mlm_server(self, program_key: str, user_id: int):
        program = PROGRAMS.get(program_key)
        upgrade_url = program.get('upgrade_url')
        mlm_server_id = program.get('mlm_server_id')
        if not upgrade_url:
            logger.warning("Upgrade URL not configured for program %s", program_key)
            return

        # Получаем API ключ для MLM сервера
        api_key = settings.MLM_SERVER_API_KEYS.get(mlm_server_id, '')
        if not api_key:
            logger.error("API key not found for MLM server %s", mlm_server_id)
            return

        payload = {'user_id': user_id, 'program': program_key}
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }

        def _post():
            response = requests.post(upgrade_url, json=payload, headers=headers, timeout=20)
            response.raise_for_status()
            return response.json()

        try:
            await asyncio.to_thread(_post)
            logger.info("MLM server %s notified about user %s", program_key, user_id)
        except requests.RequestException as exc:
            logger.error("Failed to notify MLM server %s: %s", program_key, exc)

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Глобальный обработчик ошибок"""
        logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
        
        # Попытка отправить сообщение об ошибке пользователю
        if update and isinstance(update, Update) and update.effective_message:
            try:
                await update.effective_message.reply_text(
                    "Произошла ошибка. Попробуйте позже или обратитесь в поддержку."
                )
            except Exception as e:
                logger.error(f"Error sending error message to user: {e}")

    def run(self):
        """Запуск бота"""
        if not self.application:
            logger.error("Bot not setup, cannot run")
            return

        logger.info("Starting Telegram bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


# Глобальный экземпляр бота
bot = TelegramBot()

