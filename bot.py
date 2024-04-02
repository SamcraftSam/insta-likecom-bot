from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

import hashlib

# Хэш пароля для сравнения
PASSWORD_HASH = '5f4dcc3b5aa765d61d8327deb882cf99'  # это для пароля 'password'

# Флаг, показывающий, авторизован ли пользователь
authorized = False

# Функция обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Введите пароль:")

# Функция для проверки пароля и авторизации пользователя
def check_password(update: Update, context: CallbackContext) -> None:
    global authorized
    password = update.message.text
    password_hash = hashlib.md5(password.encode()).hexdigest()

    if password_hash == PASSWORD_HASH:
        authorized = True
        update.message.reply_text("Вы успешно авторизованы!")
    else:
        update.message.reply_text("Неверный пароль, попробуйте снова.")

# Функция для обработки нажатия кнопок
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == 'start':
        query.answer()
        query.edit_message_text(text="Bot started 🟢")
    elif query.data == 'stop':
        query.answer()
        query.edit_message_text(text="Bot stopped 🔴")
    elif query.data == 'status':
        query.answer()
        query.edit_message_text(text="Status: running 🟢")
    elif query.data == 'update':
        query.answer()
        query.edit_message_text(text="Config updated ✅")

# Функция для создания клавиатуры с кнопками
def create_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Start bot ▶️", callback_data='start')],
        [InlineKeyboardButton("Stop bot ⏹", callback_data='stop')],
        [InlineKeyboardButton("Get Status ℹ️", callback_data='status')],
        [InlineKeyboardButton("Update config 🔄", callback_data='update')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Функция для отправки клавиатуры с кнопками пользователю
def send_keyboard(update: Update, context: CallbackContext) -> None:
    global authorized
    if not authorized:
        update.message.reply_text("Сначала авторизуйтесь.")
        return

    keyboard = create_keyboard()
    update.message.reply_text("Выберите действие:", reply_markup=keyboard)

def main() -> None:
    updater = Updater("YOUR_TOKEN_HERE")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("send_keyboard", send_keyboard))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
