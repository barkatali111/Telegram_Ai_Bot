# handlers.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from services import get_ai_chat_response, remove_bg, change_voice
from config import OPENAI_API_KEY, REMOVE_BG_API_KEY, VOICE_CHANGER_API_URL

def start(update: Update, context: CallbackContext):
    if update.message.chat.type in [update.message.chat.GROUP, update.message.chat.SUPERGROUP]:
        keyboard = [
            [InlineKeyboardButton("AI Chat", callback_data='chat')],
            [InlineKeyboardButton("Text to Video", callback_data='text_to_video')],
            [InlineKeyboardButton("Image to Video", callback_data='image_to_video')],
            [InlineKeyboardButton("Voice Changer", callback_data='voice_changer')],
            [InlineKeyboardButton("Remove Background", callback_data='remove_bg')],
            [InlineKeyboardButton("Photo Editor", callback_data='photo_editor')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Choose an option:', reply_markup=reply_markup)
    else:
        update.message.reply_text("This bot can only be used in a group.")

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.message.chat.type in [query.message.chat.GROUP, query.message.chat.SUPERGROUP]:
        choice = query.data
        if choice == 'chat':
            query.edit_message_text(text="Send me a message and I'll chat with you!")
        elif choice == 'text_to_video':
            query.edit_message_text(text="Send me the text and I'll convert it to video!")
        elif choice == 'image_to_video':
            query.edit_message_text(text="Send me the image and I'll convert it to video!")
        elif choice == 'voice_changer':
            query.edit_message_text(text="Send me an audio file and I'll change its voice!")
        elif choice == 'remove_bg':
            query.edit_message_text(text="Send me the image and I'll remove the background!")
        elif choice == 'photo_editor':
            query.edit_message_text(text="Send me the photo and I'll edit it for you!")
    else:
        query.answer("This bot can only be used in a group.")

def handle_message(update: Update, context: CallbackContext):
    if update.message.chat.type in [update.message.chat.GROUP, update.message.chat.SUPERGROUP]:
        if update.message.text:
            response = get_ai_chat_response(update.message.text, OPENAI_API_KEY)
            update.message.reply_text(response)
        elif update.message.photo:
            file = update.message.photo[-1].get_file()
            file.download('temp_photo.jpg')
            remove_bg('temp_photo.jpg', REMOVE_BG_API_KEY)
            with open('temp_photo_no_bg.png', 'rb') as photo:
                update.message.reply_photo(photo)
        elif update.message.video:
            update.message.reply_text("Image to Video functionality is under development!")
        elif update.message.voice:
            file = update.message.voice.get_file()
            file.download('temp_voice.ogg')
            change_voice('temp_voice.ogg', 'temp_voice_changed.ogg')
            with open('temp_voice_changed.ogg', 'rb') as voice:
                update.message.reply_voice(voice)
        elif update.message.document:
            update.message.reply_text("Photo Editor and Text to Video functionalities are under development!")
    else:
        update.message.reply_text("This bot can only be used in a group.")
