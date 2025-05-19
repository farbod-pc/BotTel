from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from googletrans import Translator
import datetime
import logging

BOT_TOKEN = 'توکن_ربات_اینجا'

translator = Translator()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    update.message.reply_text("سلام! هر متن انگلیسی که بفرستی به فارسی ترجمه می‌کنم. همچنین هر فایلی که ارسال کنی لینک دانلود مستقیمش رو می‌فرستم.")

def translate_to_farsi(update, context):
    user_message = update.message.text
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "NoUsername"
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # ذخیره پیام کاربر (اختیاری)
    with open("user_messages.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] ID:{user_id} Username:{username} Message: {user_message}\n")

    try:
        translated = translator.translate(user_message, dest='fa')
        update.message.reply_text(f"📘 ترجمه:\n{translated.text}")
    except Exception as e:
        logging.error(e)
        update.message.reply_text("❌ خطا در ترجمه!")

def handle_file(update, context):
    file = None

    if update.message.document:
        file = update.message.document.get_file()
    elif update.message.video:
        file = update.message.video.get_file()
    elif update.message.audio:
        file = update.message.audio.get_file()
    elif update.message.voice:
        file = update.message.voice.get_file()
    elif update.message.photo:
        file = update.message.photo[-1].get_file()
    else:
        update.message.reply_text("فایل پشتیبانی نمی‌شود یا پیام فایل نیست.")
        return

    file_path = file.file_path
    # لینک مستقیم دانلود فایل
    download_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    update.message.reply_text(f"لینک دانلود مستقیم فایل:\n{download_link}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_to_farsi))
    dp.add_handler(MessageHandler(Filters.document | Filters.video | Filters.audio | Filters.voice | Filters.photo, handle_file))

    print("ربات فعال شد...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
