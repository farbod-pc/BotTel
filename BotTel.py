from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import File
from googletrans import Translator
import datetime

BOT_TOKEN = 'توکن_ربات_اینجا'

translator = Translator()

# ⬅️ پیام خوش‌آمد هنگام استارت
def start(update, context):
    update.message.reply_text("سلام 👋\nبه ربات ترجمه خوش آمدید!\nمتنت رو بفرست تا برات ترجمه کنم.")

# ⬅️ ترجمه متن‌های ارسالی
def translate_to_farsi(update, context):
    user_message = update.message.text
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "NoUsername"
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # ذخیره پیام در فایل
    with open("user_messages.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] ID:{user_id} Username:{username} Message: {user_message}\n")

    try:
        translated = translator.translate(user_message, dest='fa')
        update.message.reply_text(f"📘 ترجمه:\n{translated.text}")
    except Exception as e:
        print(e)
        update.message.reply_text("❌ خطا در ترجمه!")

# ⬅️ ارسال لینک فایل
def handle_files(update, context):
    file = None

    if update.message.document:
        file = update.message.document
    elif update.message.video:
        file = update.message.video
    elif update.message.audio:
        file = update.message.audio
    elif update.message.photo:
        file = update.message.photo[-1]  # آخرین سایز (بزرگ‌ترین)

    if file:
        file_id = file.file_id
        new_file = context.bot.get_file(file_id)
        update.message.reply_text(f"📎 لینک فایل شما:\n{new_file.file_path}")
    else:
        update.message.reply_text("❗فایل قابل پردازش نبود.")

# ⬅️ اجرای اصلی ربات
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_to_farsi))
    dp.add_handler(MessageHandler(Filters.document | Filters.video | Filters.audio | Filters.photo, handle_files))

    print("✅ ربات فعال شد...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
