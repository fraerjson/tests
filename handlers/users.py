from datetime import datetime

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import re

from services.event_playground import event_service
from states.tier_state import RegistrationState, AuthorizationState, MenuState
from utils.json_to_text import convert_to_text
from aiogram import Dispatcher, types

from bot_creation import bot

def def_menu_kb():
    menu_kb = types.InlineKeyboardMarkup(row_width=1)
    menu_kb.add(types.InlineKeyboardButton("Рынок", callback_data="market"))
    menu_kb.add(types.InlineKeyboardButton("Перевод", callback_data="translation"))
    menu_kb.add(types.InlineKeyboardButton("Основные", callback_data="main"))
    menu_kb.add(types.InlineKeyboardButton("Изменить пароль", callback_data="сhange_password"))
    menu_kb.add(types.InlineKeyboardButton("Выход", callback_data="out"))
    menu_kb.add(types.InlineKeyboardButton("Вопросы и пожелания", callback_data="questions"))
    return menu_kb


"""
ВХОД
"""
telegram_id = {}


async def authorization(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AuthorizationState.number.state)

    await callback.message.answer("Введите номер телефона: ")


async def get_number(msg: types.Message, state: FSMContext):
    phone_test = msg.text
    result = re.match(r'^(\+375|80|375)(29|25|44|33)(\d{3})(\d{2})(\d{2})$', phone_test)
    if bool(result) == True:
        await state.update_data(phone_number=msg.text)
        await state.set_state(AuthorizationState.password.state)
        await msg.answer("Введите свой пароль ")
    else:
        await msg.answer("Введите коректные данные: ")


async def get_password(msg: types.Message, state: FSMContext):
    await state.update_data(password=msg.text)
    authorization_data = await state.get_data()
    user = event_service.authorization(authorization_data)
    if len(user) >= 1:
        telegram_id[msg.from_user.id] = user[0]['id']
        await msg.answer("qwe", reply_markup=def_menu_kb())
    else:
        await msg.answer("Еблан, введи норм данные")
        await state.set_state(AuthorizationState.number.state)
        await msg.answer("Введите номер телефона: ")


"""
РЕГИСТРАЦИЯ
"""


async def registration(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationState.fio.state)
    await callback.message.answer("Введите ФИО: ")


async def get_fio(msg: types.Message, state: FSMContext):
    if len(msg.text.split()) == 3:
        await state.update_data(fio=msg.text)
        await state.set_state(RegistrationState.phone.state)
        await msg.answer("Введите номер телефона: ")
    else:
        await msg.answer("Введите коректные данные: ")


async def get_phone(msg: types.Message, state: FSMContext):
    phone_test = msg.text
    result = re.match(r'^(\+375|80|375)(29|25|44|33)(\d{3})(\d{2})(\d{2})$', phone_test)
    if bool(result) == True:
        await state.update_data(phone=msg.text)
        await state.set_state(RegistrationState.email.state)
        await msg.answer("Введите Email: ")
    else:
        await msg.answer("Введите коректные данные: ")


async def get_email(msg: types.Message, state: FSMContext):
    email_test = msg.text
    result = re.match(r'^([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email_test)
    if bool(result) == True:
        await state.update_data(email=msg.text)
        await state.set_state(RegistrationState.title_company.state)
        await msg.answer("Введите название компании: ")
    else:
        await msg.answer("Введите коректные данные: ")


async def get_title_company(msg: types.Message, state: FSMContext):
    await state.update_data(title_company=msg.text)
    await state.set_state(RegistrationState.revenue.state)
    await msg.answer("Введите выручку компании: ")


async def get_revenue(msg: types.Message, state: FSMContext):
    await state.update_data(user_id=msg.from_user.id)
    await state.update_data(first_name=msg.from_user.first_name)
    await state.update_data(nickname=msg.from_user.username)
    await state.update_data(revenue=msg.text)
    User_data = await state.get_data()
    User = event_service.create_User(User_data)
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Продолжить", callback_data="start_1"))
    await msg.answer("Вы успешно вошли в учетнуя запись, для продолжения нажмите кнопку 'Продолжить'",
                     reply_markup=inline_kb)
    telegram_id[msg.from_user.id] = User[0]['id']
    await msg.answer("Рады приветствовать вас в этой поеботине вот наше меню:", reply_markup=menu_kb())


"""
РАССЦЕНКИ
"""

async def description(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationState.fio.state)
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Return", callback_data="return"))
    await callback.message.edit_text("Описание: \n\nТут нихуя нету, иди нахуй", reply_markup=inline_kb)


"""
МЕНЮ
"""




async def market(callback: types.CallbackQuery, state: FSMContext):
    print("qwe")
    await callback.message.answer("Тут нихуя нету, иди нахуй")






def setup(dp: Dispatcher):
    """
    ВХОД
    """
    dp.register_message_handler(get_number, state=AuthorizationState.number)
    dp.register_message_handler(get_password, state=AuthorizationState.password)

    """
    НАЧАЛЬНОЕ МЕНЮ
    """
    dp.register_callback_query_handler(authorization, Text(contains="authorization"))
    dp.register_callback_query_handler(registration, Text(contains="registration"))
    dp.register_callback_query_handler(description, Text(contains="description"))

    """
    ГЛАВНОЕ МЕНЮ
    """
    dp.register_callback_query_handler(market, Text(contains="market"))

    dp.register_message_handler(get_fio, state=RegistrationState.fio)
    dp.register_message_handler(get_phone, state=RegistrationState.phone)
    dp.register_message_handler(get_email, state=RegistrationState.email)
    dp.register_message_handler(get_title_company, state=RegistrationState.title_company)
    dp.register_message_handler(get_revenue, state=RegistrationState.revenue)




