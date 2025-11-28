"""
Задачи для бота (для использования с Celery, если нужно)
"""
from telegram import Bot
from django.conf import settings
import logging
import asyncio

logger = logging.getLogger(__name__)


def send_telegram_message(telegram_id: int, message: str):
    """Отправить сообщение пользователю через Telegram"""
    try:
        async def send():
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            await bot.send_message(chat_id=telegram_id, text=message)
        
        asyncio.run(send())
    except Exception as e:
        logger.error(f"Error sending telegram message: {e}")

