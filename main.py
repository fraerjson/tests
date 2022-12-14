import logging

from aiogram import Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.users import setup as user_handler_setup
from services.event_playground import event_service
from bot_creation import bot


logging.basicConfig(level=logging.INFO)

dp = Dispatcher(bot, storage=MemoryStorage())


async def startup(_):
    event_service.check_availability()


@dp.message_handler(commands=["start"])
async def get_admin_commands(msg: types.Message):
    # await msg.answer('Проверка', reply_markup=types.ReplyKeyboardRemove())
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Вход", callback_data="authorization"))
    inline_kb.add(types.InlineKeyboardButton("Регистрация", callback_data="registration"))
    inline_kb.add(types.InlineKeyboardButton("Описание", callback_data="description"))
    await msg.answer("Choose admin action", reply_markup=inline_kb)


@dp.message_handler(commands=["come"])
async def get_admin_commands(msg: types.Message):
    menu_kb = types.InlineKeyboardMarkup(row_width=1)
    # menu_kb.add(types.ReplyKeyboardRemove)
    menu_kb.add(types.InlineKeyboardButton("Рынок", callback_data="market"))
    menu_kb.add(types.InlineKeyboardButton("Перевод", callback_data="translation"))
    menu_kb.add(types.InlineKeyboardButton("Основные", callback_data="main"))
    menu_kb.add(types.InlineKeyboardButton("Изменить пароль", callback_data="сhange_password"))
    menu_kb.add(types.InlineKeyboardButton("Вопросы и пожелания", callback_data="questions"))
    menu_kb.add(types.InlineKeyboardButton("Выход", callback_data="out"))
    await msg.answer("Главное меню: ", reply_markup=menu_kb)


@dp.callback_query_handler(Text(contains="description"))
async def market(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("В главное меню", callback_data="home"))
    await callback.message.answer("Тут нихуя нету, иди нахуй", reply_markup=inline_kb)

@dp.callback_query_handler(Text(contains="home"))
async def return_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Вход", callback_data="authorization"))
    inline_kb.add(types.InlineKeyboardButton("Регистрация", callback_data="registration"))
    inline_kb.add(types.InlineKeyboardButton("Описание", callback_data="description"))
    await callback.message.answer("Choose admin action", reply_markup=inline_kb)


user_handler_setup(dp)
executor.start_polling(dp, skip_updates=True, on_startup=startup)