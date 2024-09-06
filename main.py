# main.py

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from handlers import start, button, handle_message
from config import TELEGRAM_API_TOKEN

def main():
    updater = Updater(TELEGRAM_API_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.photo, handle_message))
    dp.add_handler(MessageHandler(Filters.video, handle_message))
    dp.add_handler(MessageHandler(Filters.voice, handle_message))
    dp.add_handler(MessageHandler(Filters.document, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
