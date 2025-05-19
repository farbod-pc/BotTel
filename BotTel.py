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
        "سلام! من ربات ترجمه و لینک فایل هستم.\n"
        "هر متنی بفرست تا برات ترجمه کنم و هر فایلی بفرستی لینک دانلودش رو می‌دم."
    )

def translate_to_farsi(update, context):
    user_message = update.message.text
    try:
        translated = translator.translate(user_message, dest='fa')
        update.message.reply_text(f"📘 ترجمه:\n{translated.text}")
    except Exception as e:
        logging.error(f"خطا در ترجمه: {e}")
        update.message.reply_text("❌ خطا در ترجمه!")

def handle_file(update, context):
    message = update.message
    file = None

    if message.document:
        file = message.document.get_file()
    elif message.video:
        file = message.video.get_file()
    elif message.audio:
        file = message.audio.get_file()
    elif message.voice:
        file = message.voice.get_file()
    elif message.photo:
        # عکس ها یک لیست هستند، بزرگترین (آخرین) را انتخاب می‌کنیم
        file = message.photo[-1].get_file()
    else:
        update.message.reply_text("❗ این نوع فایل پشتیبانی نمی‌شود.")
        return

    try:
        file_path = file.file_path  # مسیر فایل روی سرور تلگرام
        download_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        update.message.reply_text(f"✅ لینک دانلود فایل:\n{download_link}")
    except Exception as e:
        logging.error(f"خطا در دریافت لینک فایل: {e}")
        update.message.reply_text("❌ خطا در دریافت لینک فایل!")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_to_farsi))
    dp.add_handler(MessageHandler(
        Filters.document | Filters.video | Filters.audio | Filters.voice | Filters.photo,
        handle_file
    ))

    print("ربات فعال شد...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
