from telegram.ext import Updater, MessageHandler, Filters
from googletrans import Translator
import datetime

BOT_TOKEN = '7869080937:AAGIC4et9wB0E2wGLfLfqFCMRVdet8_PyR8'

translator = Translator()

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

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_to_farsi))

    print("ربات فعال شد...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
