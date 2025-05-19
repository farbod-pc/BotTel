from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from googletrans import Translator
from gtts import gTTS
import datetime
import os

BOT_TOKEN = 'توکن خودت اینجا'

translator = Translator()

# تابع خوش‌آمد برای /start
def start(update, context):
    update.message.reply_text("سلام! 👋 به ربات مترجم خوش آمدی.\nمتنت رو بفرست تا برات ترجمه کنم و ویس هم بفرستم.")

# تابع ترجمه و تولید ویس
def translate_to_farsi(update, context):
    user_message = update.message.text
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "NoUsername"
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # ذخیره پیام
    with open("user_messages.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] ID:{user_id} Username:{username} Message: {user_message}\n")

    try:
        translated = translator.translate(user_message, dest='fa')
        update.message.reply_text(f"📘 ترجمه:\n{translated.text}")

        # تولید ویس زبان اصلی
        tts = gTTS(text=user_message, lang=translated.src)  # زبان اصلی شناسایی‌شده
        audio_path = f"voice_{user_id}.mp3"
        tts.save(audio_path)

        # ارسال فایل صوتی
        with open(audio_path, 'rb') as audio_file:
            update.message.reply_voice(audio=audio_file)

        os.remove(audio_path)

    except Exception as e:
        print("خطا:", e)
        update.message.reply_text("❌ خطا در ترجمه یا تولید ویس!")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_to_farsi))

    print("ربات فعال شد...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
