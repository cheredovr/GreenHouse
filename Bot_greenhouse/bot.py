from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import Updater, CommandHandler, CallbackContext

# 🔐 Вставь сюда токен своего бота от @BotFather
BOT_TOKEN = "7607901680:AAGvfP5AABJcuuP-qJNwFnpzYBryGbzusbY"

# 🔗 URL твоего Telegram Web App (например, с GitHub Pages)
WEB_APP_URL = "https://your-username.github.io/telegram-webapp-demo/"

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    # Кнопка "START" с привязкой WebApp
    keyboard = [
        [KeyboardButton(text="START", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=True
    )

    context.bot.send_message(
        chat_id=chat_id,
        text="Нажми кнопку START, чтобы открыть приложение 👇",
        reply_markup=reply_markup
    )

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    print("Бот запущен. Нажми Ctrl+C для остановки.")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
