from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import json
from googletrans import Translator

BOT_TOKEN = '7869080937:AAGIC4et9wB0E2wGLfLfqFCMRVdet8_PyR8'

translator = Translator()

# 📌 فایل شمارنده پیام کاربران
USER_COUNT_FILE = "user_message_count.json"

def load_counts():
    try:
        with open(USER_COUNT_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_counts(counts):
    with open(USER_COUNT_FILE, 'w') as f:
        json.dump(counts, f)

# ✅ هندلر start
def start(update, context):
    update.message.reply_text("سلام 👋 خوش اومدی! هر متنی که خواستی بفرست تا برات ترجمه کنم.")

# ✅ هندلر ترجمه پیام
def translate_to_farsi(update, context):
    user_message = update.message.text
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "NoUsername"
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 🔹 ثبت تعداد پیام‌ها
    counts = load_counts()
    counts[user_id] = counts.get(user_id, 0) + 1
    save_counts(counts)

    # 🔹 ذخیره در فایل ساده
    with open("user_messages.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] ID:{user_id} Username:{username} Message: {user_message}\n")

    # 🔹 پاسخ به برخی کلمات خاص
    if user_message.lower() == "سلام":
        update.message.reply_text("سلام عزیزم 😊")
        return
    elif user_message.lower() == "خداحافظ":
        update.message.reply_text("فعلاً! مراقب خودت باش 😇")
        return

    # 🔹 ترجمه و ارسال
    try:
        translated = translator.translate(user_message, dest='fa')
        response = f"📘 ترجمه:\n{translated.text}\n\n🕓 زمان دریافت: {now}\n📩 تعداد پیام‌های شما: {counts[user_id]}"
        update.message.reply_text(response)
    except Exception as e:
        print(e)
        update.message.reply_text("❌ خطا در ترجمه!")

# ✅ راه‌اندازی ربات
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
