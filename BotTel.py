from telegram.ext import Updater, MessageHandler, Filters
import logging

BOT_TOKEN = '7869080937:AAGIC4et9wB0E2wGLfLfqFCMRVdet8_PyR8'

# فعال کردن لاگ برای دیباگ راحت‌تر
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def file_handler(update, context):
    message = update.message

    # بررسی نوع فایل
    file_object = (
        message.document or
        message.video or
        message.audio or
        message.voice
    )

    if file_object:
        file_id = file_object.file_id
        file = context.bot.get_file(file_id)
        file_link = file.file_path

        update.message.reply_text(f"📥 لینک دانلود فایل:\n{file_link}")
    else:
        update.message.reply_text("❗ لطفاً یک فایل (ویدیو، صوتی یا سند) ارسال کنید.")

def start_handler(update, context):
    update.message.reply_text("👋 سلام! لطفاً فایل خود را ارسال کنید تا لینک آن را دریافت کنید.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # هندلر برای شروع /start
    dp.add_handler(MessageHandler(Filters.command & Filters.regex('^/start$'), start_handler))

    # هندلر برای انواع فایل‌ها
    dp.add_handler(MessageHandler(
        Filters.document | Filters.video | Filters.audio | Filters.voice,
        file_handler
    ))

    print("✅ ربات فعال شد.")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
