import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import os
from dotenv import load_dotenv
import logging


# Определение состояний
class OrderStatusForm(StatesGroup):
    waiting_for_order_id = State()

load_dotenv()
TOKEN = os.getenv('TGB_TOKEN')

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher( storage=storage)

logging.basicConfig(level=logging.INFO)

DJANGO_API_URL = 'http://digidobu.beget.tech/api/order_status/'

def create_main_menu():
    btn1 = KeyboardButton(text='Как заказать букет')
    btn2 = KeyboardButton(text='Проверить статус заказа')
    markup = ReplyKeyboardMarkup(keyboard=[[btn1, btn2]], resize_keyboard=True)
    return markup

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    markup = create_main_menu()
    await message.answer("Добро пожаловать в нашу цветочную студию!", reply_markup=markup)

@dp.message(Command("help"))
async def send_help(message: types.Message):
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
    await message.answer(help_text)

@dp.message(Command("status"))
async def handle_status_command(message: types.Message, state: FSMContext):
    command_parts = message.text.split()
    print(f'command_parts: {command_parts}')
    if len(command_parts) > 1:
        order_id = command_parts[1]
        await check_order_status_by_id(message, order_id)
    else:
        await message.answer("Пожалуйста, введите номер вашего заказа:")
        await state.set_state(OrderStatusForm.waiting_for_order_id)

# Обработчик ввода номера заказа
@dp.message(OrderStatusForm.waiting_for_order_id)
async def process_order_id(message: types.Message, state: FSMContext):
    order_id = message.text.strip()
    if order_id.isdigit():
        await check_order_status_by_id(message, order_id)
    else:
        await message.answer("Некорректный номер заказа. Пожалуйста, введите правильный номер заказа:")
        await state.set_state(OrderStatusForm.waiting_for_order_id)


@dp.message(lambda message: message.text)
async def handle_message(message: types.Message):
    if message.text == 'Как заказать букет' or message.text == '/info':
        await message.answer("Для заказа букетов перейдите на наш сайт: http://digidobu.beget.tech/")
    elif message.text == 'Проверить статус заказа':
        await message.answer("Пожалуйста, введите номер вашего заказа:")
    else:
        markup = create_main_menu()
        await message.answer(
            "Пожалуйста, выберите одну из предложенных опций или используйте /help для получения списка команд.", reply_markup=markup)


async def check_order_status_by_id(message: types.Message, order_id: str):
    print(f'1. order_id: {order_id}')
    async with aiohttp.ClientSession() as session:
        print(f'2. img_url: {DJANGO_API_URL}{order_id}/')
        async with session.get(f"{DJANGO_API_URL}{order_id}/") as response:
            print(f'3. response: {response}')
            if response.status == 200:
                order_info = await response.json()
                await message.answer(
                    f"Заказ №{order_info['id']}:\nСтатус: {order_info['status']}\nАдрес доставки: {order_info['delivery_address']}"
                )

                for item in order_info['items']:
                    image_url = f"http://digidobu.beget.tech/flower_mosaic/media/{item['image']}"
                    try:
                        await bot.send_photo(
                            message.chat.id, image_url,
                            caption=f"{item['product_name']}: {item['quantity']} шт. по {item['price']} руб."
                        )
                    except Exception as e:
                        await message.answer(
                            f"{item['product_name']}: {item['quantity']} шт. по {item['price']} руб.\n(Изображение недоступно)"
                        )
            else:
                await message.answer("Заказ с таким номером не найден. Пожалуйста, попробуйте снова.")

    markup = create_main_menu()
    await message.answer("Выберите действие:", reply_markup=markup)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
