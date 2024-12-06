import telebot
import requests
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TGB_TOKEN')
bot = telebot.TeleBot(TOKEN)

DJANGO_API_URL = 'http://digidobu.beget.tech/api/order_status/'

def create_main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Как заказать букет')
    btn2 = telebot.types.KeyboardButton('Проверить статус заказа')
    markup.add(btn1, btn2)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = create_main_menu()
    bot.send_message(message.chat.id, "Добро пожаловать в нашу цветочную студию!", reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Вот список доступных команд:\n"
        "/start - Начать взаимодействие с ботом\n"
        "/help - Получить помощь и список команд\n"
        "/info - Как заказать букет\n"
        "/status <номер заказа> - Проверить статус заказа\n"
        "Вы также можете использовать кнопки для навигации:\n"
        "- Как заказать букет\n"
        "- Проверить статус заказа\n"
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['status'])
def handle_status_command(message):
    command_parts = message.text.split()
    if len(command_parts) > 1:
        order_id = command_parts[1]
        check_order_status_by_id(message, order_id)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите номер вашего заказа:")
        bot.register_next_step_handler(message, check_order_status)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Как заказать букет' or message.text == '/info':
        bot.send_message(message.chat.id, "Для заказа букетов перейдите на наш сайт: http://digidobu.beget.tech/")
    elif message.text == 'Проверить статус заказа':
        bot.send_message(message.chat.id, "Пожалуйста, введите номер вашего заказа:")
        bot.register_next_step_handler(message, check_order_status)
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, выберите одну из предложенных опций или используйте /help для получения списка команд.")

def check_order_status(message):
    order_id = message.text
    check_order_status_by_id(message, order_id)

def check_order_status_by_id(message, order_id):
    response = requests.get(f"{DJANGO_API_URL}{order_id}/")
    if response.status_code == 200:
        order_info = response.json()
        bot.send_message(message.chat.id,
                         f"Заказ №{order_info['id']}:\nСтатус: {order_info['status']}\nАдрес доставки: {order_info['delivery_address']}")

        for item in order_info['items']:
            image_url = f"http://digidobu.beget.tech/flower_mosaic/media/{item['image']}"  # Предполагается, что изображения хранятся в этой директории
            try:
                bot.send_photo(message.chat.id, image_url,
                               caption=f"{item['product_name']}: {item['quantity']} шт. по {item['price']} руб.")
            except Exception as e:
                bot.send_message(message.chat.id,
                                 f"{item['product_name']}: {item['quantity']} шт. по {item['price']} руб.\n(Изображение недоступно)")
    else:
        bot.send_message(message.chat.id, "Заказ с таким номером не найден. Пожалуйста, попробуйте снова.")

    # Повторное отображение основного меню
    markup = create_main_menu()
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

bot.polling()