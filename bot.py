import telebot
from telebot import types
import hashlib

with open("token.txt", "r") as t:
    bot_secret = t.readlines()[0]


bot = telebot.TeleBot(bot_secret)

# Хэш пароля (пример: хэш от 'password123')
PASSWORD_HASH = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'

BUTTON_RUN_TEXT = 'Start the bot'
BUTTON_GET_HELP = 'Help'
BUTTON_SET_ACCOUNTS = 'Paste accounts in format: nickname password'
BUTTON_SET_TARGETS = 'Paste targeted accounts(one per line)'
BUTTON_SET_COMMENTS = 'Paste comments(one per line)'
DOCUMENTATION = 'some extra info will be provided soon...'


logged_in = False

@bot.message_handler(commands=['start']) #на команду старт
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Hi!")
    markup.add(btn1)
    msg = bot.send_message(message.from_user.id, "Hello!👋 To proceed, please login:", reply_markup=markup)
    bot.register_next_step_handler(msg, check_password)

@bot.message_handler(commands=['cancel'])
def cancel(message):
    bot.send_message(message.chat.id, "'/cancel' request detected!")
    

# Проверка пароля
def check_password(message):
    global logged_in

    password = message.text
    if hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH:
        bot.send_message(message.chat.id, 'Login succesful!')
        logged_in = True
        show_buttons(message)
    else:
        bot.send_message(message.chat.id, 'Incorrect password :( Try again!')
        request_password(message)

def update_accounts(message):
    try:
        if not '/cancel' in message.text:
            with open("accounts.txt", "w") as f:
                f.write(message.text)
            bot.send_message(message.chat.id, "data updated!")
        else:
            cancel(message)
    except Exception as ex:
        bot.send_message(message.chat.id, f'{ex} \nPlease report it to the app developer: anon_h4c3k3r@proton.me')
        print(ex)
        return

def update_targets(message):
    try:
        if not '/cancel' in message.text:    
            with open("targets.txt", "w") as t:
                t.write(message.text)
            bot.send_message(message.chat.id, "data updated!")
        else:
            cancel(message)

    except Exception as ex:
        bot.send_message(message.chat.id, f'{ex} \nPlease report it to the app developer: anon_h4c3k3r@proton.me')
        print(ex)
        return

# Запрос пароля
def request_password(message):
    msg = bot.send_message(message.chat.id, 'Enter the password:')
    bot.register_next_step_handler(msg, check_password)

# Показ кнопок
def show_buttons(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button_run = types.KeyboardButton(BUTTON_RUN_TEXT)
    button2 = types.KeyboardButton(BUTTON_GET_HELP)
    button3 = types.KeyboardButton(BUTTON_SET_TARGETS)
    button4 = types.KeyboardButton(BUTTON_SET_ACCOUNTS)
    markup.add(button_run, button2, button3, button4)
    bot.send_message(message.chat.id, 'Push some buttons:', reply_markup=markup)

# Обработка нажатий на кнопки
@bot.message_handler(func=lambda message: True)
def button_pressed(message):

    if not logged_in:
        bot.send_message(message.chat.id, 'Please log in first!!!')
        request_password(message)
        return
    
    if message.text == BUTTON_SET_ACCOUNTS:
        try:
            accs = ''
            with open("accounts.txt", "r") as a:
                accs = a.read()

            bot.send_message(message.chat.id, f'Your current accounts list:\n\n {accs}')

        except Exception as ex:
            bot.send_message(message.chat.id, f'{ex} \nPlease report it to the app developer: anon_h4c3k3r@proton.me')
            print(ex)
            return

        msg = bot.send_message(message.chat.id, 'Paste credentials here: \n(separated by space, one pair by line)\nNotice that you will overwrite previous file. Also, do not forget to authorize login via e-mail\n/cancel to cancel operation')
        bot.register_next_step_handler(msg, update_accounts)

    if message.text == BUTTON_GET_HELP:
        bot.send_message(message.chat.id, DOCUMENTATION)

    if message.text == BUTTON_SET_TARGETS: 
        try:
            accs = ''
            with open("targets.txt", "r") as a:
                accs = a.read()

            bot.send_message(message.chat.id, f'Your current targets:\n\n {accs}')

        except Exception as ex:
            bot.send_message(message.chat.id, f'{ex} \nPlease report it to the app developer: anon_h4c3k3r@proton.me')
            print(ex)
            return

        msg = bot.send_message(message.chat.id, f'Paste targets here: \n(one target per line)\nNotice that you will overwrite previous file!\n/cancel to cancel operation')
        bot.register_next_step_handler(msg, update_targets)


# Запуск бота
bot.polling(none_stop=True)
