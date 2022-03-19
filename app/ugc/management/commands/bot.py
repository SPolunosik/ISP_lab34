from django.core.management.base import BaseCommand
from telegram import Bot
from telegram.ext import Filters
from telegram.ext import MessageHandler, CommandHandler
from telegram.ext import Updater
from telegram.utils.request import Request
from .handler import *
import logging
import os
from . import *

class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):

        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        
        bot = Bot(
            request=request,
            token=TOKEN,
            base_url=PROXY_URL,
        )

        updater = Updater(
            bot=bot,
            use_context=True,
        )

        print(bot.get_me())

        dp = updater.dispatcher
        dp.add_handler(CommandHandler(
            'start', start_bot_callback))
        dp.add_handler(CommandHandler(
            'show', show_item_callback))

        dp.add_handler(
            CommandHandler
            (
                'create',
                create_item_callback,
                filters=Filters.user(username=ADMIN_USER)
            )
        )
        dp.add_handler(CommandHandler('update', update_item_callback,
                       filters=Filters.user(username=ADMIN_USER)))
        dp.add_handler(CommandHandler('delete', delete_item_callback,
                       filters=Filters.user(username=ADMIN_USER)))
        dp.add_handler(CommandHandler('buy',buy_item_callback))
        dp.add_handler(MessageHandler(
            Filters.command, unknown_command_callback))

        updater.start_polling()
        updater.idle()
