"""
Django management command для запуска Telegram бота
"""
import logging
import asyncio
from django.core.management.base import BaseCommand
from django.conf import settings
from bot.bot import bot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **options):
        self.stdout.write("=" * 50)
        self.stdout.write("Initializing Telegram Bot...")
        self.stdout.write(f"TELEGRAM_BOT_TOKEN exists: {bool(settings.TELEGRAM_BOT_TOKEN)}")
        self.stdout.write("=" * 50)
        
        # Настройка бота (синхронно)
        bot.setup()
        
        if not bot.application:
            self.stdout.write(self.style.ERROR("Bot setup failed! Check TELEGRAM_BOT_TOKEN"))
            return
        
        self.stdout.write(self.style.SUCCESS("Bot setup successful, starting polling..."))
        self.stdout.write("Bot is now running and waiting for messages...")
        self.stdout.write("=" * 50)
        
        # Запуск бота (блокирующий вызов)
        bot.run()

