import telebot
import requests
from dotenv import load_dotenv
import os


load_dotenv()
TOKEN = os.getenv('TGB_TOKEN')
bot = telebot.TeleBot(TOKEN)

# URL API вашего Django веб-приложения
DJANGO_API_URL = 'http://your_django_server/api/order_status/'

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Как заказать букет')
    btn2 = telebot.types.KeyboardButton('Проверить статус заказа')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Добро пожаловать в нашу цветочную студию!", reply_markup=markup)


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Вот список доступных команд:\n"
        "/start - Начать взаимодействие с ботом\n"
        "/help - Получить помощь и список команд\n"
        "Вы также можете использовать кнопки для навигации:\n"
        "- Как заказать букет\n"
        "- Проверить статус заказа\n"
    )
    bot.send_message(message.chat.id, help_text)


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Как заказать букет':
        # bot.send_message(message.chat.id, "Для заказа букетов перейдите на наш сайт: https://flower-mosaic.com")
        bot.send_message(message.chat.id, "Для заказа букетов перейдите на наш сайт: http://127.0.0.1:8000/")
    elif message.text == 'Проверить статус заказа':
        bot.send_message(message.chat.id, "Пожалуйста, введите номер вашего заказа:")
        bot.register_next_step_handler(message, check_order_status)
    else:
        bot.send_message(message.chat.id,
        "Пожалуйста, выберите одну из предложенных опций или используйте /help для получения списка команд.")

# Функция для проверки статуса заказа
def check_order_status(message):
    order_id = message.text
    response = requests.get(f"{DJANGO_API_URL}{order_id}/")

    if response.status_code == 200:
        order_info = response.json()
        items_info = "\n".join([
            f"{item['product_name']}: {item['quantity']} шт. по {item['price']} руб."
            for item in order_info['items']
        ])
        bot.send_message(message.chat.id, f"Заказ №{order_info['order_id']}:\nСтатус: {order_info['status']}\n{items_info}")
    else:
        bot.send_message(message.chat.id, "Заказ с таким номером не найден. Пожалуйста, попробуйте снова.")

# Запуск бота
bot.polling()
