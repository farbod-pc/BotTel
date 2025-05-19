from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from googletrans import Translator
import logging

# توکن ربات خود را اینجا قرار دهید
BOT_TOKEN = '7869080937:AAGIC4et9wB0E2wGLfLfqFCMRVdet8_PyR8'

translator = Translator()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

def start(update, context):
    update.message.reply_text(
        "سلام! من ربات ترجمه هستم. هر متنی بفرست تا برات به فارسی ترجمه کنم."
    )

def translate_to_farsi(update, context):
    user_message = update.message.text
    try:
        translated = translator.translate(user_message, dest='fa')
        update.message.reply_text(f"📘 ترجمه:\n{translated.text}")
    except Exception as e:
        logging.error(f"خطا در ترجمه: {e}")
        update.message.reply_text("❌ خطا در ترجمه!")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_to_farsi))

    print("ربات ترجمه فعال شد...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
