"""
Django management command для запуска Telegram бота
"""
from django.core.management.base import BaseCommand
from bot.bot import bot


class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **options):
        bot.setup()
        bot.run()

