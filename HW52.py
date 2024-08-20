from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio
import text_to_HW52

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать норму калорий')
button2 = KeyboardButton(text='Формулы расчёта')
button3 = KeyboardButton(text='Купить')
kb.add(button)
kb.add(button2)
kb.add(button3)

catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Product1", callback_data='product_buying')],
        [InlineKeyboardButton(text="Product2", callback_data='product_buying')],
        [InlineKeyboardButton(text="Product3", callback_data='product_buying')],
        [InlineKeyboardButton(text="Product4", callback_data='product_buying')]
    ]
)


@dp.message_handler(text='Рассчитать норму калорий')
async def main_menu(message):
    await message.answer('Отлично, введите свой возраст')
    await UserState.age.set()


@dp.message_handler(text='Формулы расчёта')
async def get_formulas(message):
    await message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')


@dp.message_handler(commands=['start'])
async def start_message(message):
    print('Start message')
    await message.answer('Привет! Я бот, помогающий Вашему здоровью. Напиши Рассчитать норму калорий, чтобы начать подсчёт',
                         reply_markup=kb)


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Супер, теперь введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Ещё чуть-чуть! Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if 'age' in data and 'growth' in data and 'weight' in data:
        try:
            age = float(data['age'])
            growth = float(data['growth'])
            weight = float(data['weight'])
            norma_man = 10 * weight + 6.25 * growth - 5 * age + 5
            await message.answer(f'Ваша норма калорий - {norma_man}')
        except ValueError:
            await message.answer('Пожалуйста, введите числовые значения.')
    else:
        await message.answer('Пожалуйста, заполните все необходимые поля.')
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('files too/Апельсин.png', 'rb') as img:
        await message.answer_photo(img, f'Название: апельсин | Описание: {text_to_HW52.orange} | Цена: {text_to_HW52.orange_price}')
    with open('files too/Брокколи.png', 'rb') as img2:
        await message.answer_photo(img2, f'Название: брокколи | Описание: {text_to_HW52.broccoli} | Цена: {text_to_HW52.broccoli_price}')
    with open('files too/Морковка.png', 'rb') as img3:
        await message.answer_photo(img3, f'Название: морковь | Описание: {text_to_HW52.carrot} | Цена: {text_to_HW52.carrot_price}')
    with open('files too/Яблоко.png', 'rb') as img4:
        await message.answer_photo(img4, f'Название: яблоко | Описание: {text_to_HW52.apple} | Цена: {text_to_HW52.apple_price}')
    await message.answer('Выберите продукт для покупки', reply_markup=catalog_kb)


@dp.callback_query_handler(text='product_buying')
async def product_buying(call):
    await call.message.answer('Вы выбрали продукт для покупки. Для оформления заказа, пожалуйста, свяжитесь с нашим менеджером.')
    await call.answer()


@dp.message_handler()
async def all_message(message):
    print('Мы получили сообщение')
    await message.answer('Введите команду /start, чтобы узнать свою норму калорий (для мужчин)')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)