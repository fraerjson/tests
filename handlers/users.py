from datetime import datetime

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import re

from aiogram.types import KeyboardButton

from services.event_playground import event_service
from states.tier_state import RegistrationState, AuthorizationState, MenuState, TransferState
from utils.json_to_text import convert_to_text
from aiogram import Dispatcher, types

from bot_creation import bot


def global_menu():
    menu_kb = types.InlineKeyboardMarkup(row_width=1)
    menu_kb.add(types.InlineKeyboardButton("Рынок", callback_data="market"))
    menu_kb.add(types.InlineKeyboardButton("Перевод", callback_data="translation"))
    menu_kb.add(types.InlineKeyboardButton("Основные", callback_data="main"))
    menu_kb.add(types.InlineKeyboardButton("Изменить пароль", callback_data="сhange_password"))
    menu_kb.add(types.InlineKeyboardButton("Вопросы и пожелания", callback_data="questions"))
    menu_kb.add(types.InlineKeyboardButton("Выход", callback_data="out"))
    return menu_kb


def menu_reply():
    reply_kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    reply_kb.add(KeyboardButton('В главное меню'))
    return reply_kb

def user_menu_reply():
    reply_kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    reply_kb.add(KeyboardButton('В меню пользователя'))
    return reply_kb


def start_button():
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Вход", callback_data="authorization"))
    inline_kb.add(types.InlineKeyboardButton("Регистрация", callback_data="registration"))
    inline_kb.add(types.InlineKeyboardButton("Описание", callback_data="description"))
    return inline_kb


"""
ВХОД
"""

async def authorization(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(AuthorizationState.number.state)
    await callback.message.answer("Введите номер телефона: ", reply_markup=menu_reply())


async def get_number(msg: types.Message, state: FSMContext):
    if msg.text == 'В главное меню':
        await msg.answer("Choose admin action", reply_markup=start_button())
        await state.finish()
    else:
        phone_test = msg.text
        result = re.match(r'^(\+375|80|375)(29|25|44|33)(\d{3})(\d{2})(\d{2})$', phone_test)
        if bool(result) == True:
            await state.update_data(phone_number=msg.text)
            await state.set_state(AuthorizationState.password.state)
            await msg.answer("Введите свой пароль ")
        else:
            await msg.answer("Введите коректные данные: ")


async def get_password(msg: types.Message, state: FSMContext):
    if msg.text == 'В главное меню':
        await msg.answer("Choose admin action", reply_markup=start_button())
        await state.finish()
    else:
        await state.update_data(password=msg.text)
        authorization_data = await state.get_data()
        user = event_service.authorization(authorization_data)
        if len(user) >= 1:
            await msg.answer('Проверка', reply_markup=types.ReplyKeyboardRemove())
            await msg.answer("Главное меню", reply_markup=global_menu())
            await state.finish()
        else:
            await msg.answer("Еблан, введи норм данные")
            await state.set_state(AuthorizationState.number.state)
            await msg.answer("Введите номер телефона: ")


"""
РЕГИСТРАЦИЯ
"""


async def registration(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationState.name.state)
    await callback.message.delete()
    await callback.message.answer("Введите никнэйм: ", reply_markup=menu_reply())


async def get_name(msg: types.Message, state: FSMContext):
    if msg.text == 'В главное меню':
        await msg.answer("Choose admin action", reply_markup=start_button())
        await state.finish()
    else:
        name_test = msg.text
        result = re.match(r'[a-z0-9](?:[_.]?[a-z0-9]){3,11}$', name_test)
        if bool(result) == True:
            name_data = {'name': name_test}
            user = event_service.check_name(name_data)
            if len(user) == 0:
                await state.update_data(name=name_test)
                await state.set_state(RegistrationState.phone.state)
                await msg.answer("Введите номер телефона: ")
            else:
                await msg.answer("Такой пользователь уже существует, введите другий никнэйм")
        else:
            await msg.answer("Введите коректные данные: ")


async def get_phone(msg: types.Message, state: FSMContext):
    if msg.text == 'В главное меню':
        await msg.answer("Choose admin action", reply_markup=start_button())
        await state.finish()
    else:
        phone_test = msg.text
        result = re.match(r'^(\+375|80|375)(29|25|44|33)(\d{3})(\d{2})(\d{2})$', phone_test) # get_aut_password
        if bool(result) == True:
            phone_data = {'phone_number': phone_test}
            user = event_service.check_phone_number(phone_data)
            if len(user) == 0:
                await state.update_data(phone_number=msg.text)
                await state.set_state(RegistrationState.password.state)
                await msg.answer("Введите пароль: ")
            else:
                await msg.answer("Такой номер телефона уже зарегестрирован")
        else:
            await msg.answer("Введите коректные данные: ")

async def get_aut_password(msg: types.Message, state: FSMContext):
    if msg.text == 'В главное меню':
        await msg.answer("Choose admin action", reply_markup=start_button())
        await state.finish()
    else:
        await state.update_data(password=msg.text)
        await state.update_data(tg_id=msg.from_user.id)
        user_data = await state.get_data()
        user = event_service.create_user(user_data)

        user_data = {'tg_id': msg.from_user.id}
        users_response = event_service.get_users_id(user_data)
        print(users_response)
        for i in users_response:
            id = i['id']
        user_id = {'id': id}

        user_data = {'wallet': {
        "balance": 100000,
        "overall_balance": 100000.0,
        "bitcoin": 0.0,
        "ethereum": 0.0,
        "litecoin": 0.0,
        "binance_coin": 0.0,
        "cardano": 0.0,
        "solana": 0.0,
        "users": user_id['id']
        }}

        users_response = event_service.post_user_pk(user_data, user_id)

        await msg.answer('Проверка', reply_markup=types.ReplyKeyboardRemove())
        await msg.answer("Рады приветствовать вас в этой поеботине вот наше меню:", reply_markup=global_menu())
        await state.finish()


"""
РАССЦЕНКИ
"""

async def description(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationState.name.state)
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Return", callback_data="return"))
    await callback.message.edit_text("Описание: \n\nТут нихуя нету, иди нахуй", reply_markup=inline_kb)


"""
ГЛАВНОЕ МЕНЮ
"""

async def market(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Вернуться меню", callback_data="return_user"))
    await callback.message.answer("Тут нихуя нету, иди нахуй", reply_markup=inline_kb)


async def translation(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("USD", callback_data="usd"))
    inline_kb.add(types.InlineKeyboardButton("Криптовалюта", callback_data="cryptocurrency"))
    inline_kb.add(types.InlineKeyboardButton("Вернуться меню", callback_data="return_user"))
    await callback.message.answer("Выберите что будете переводить: ", reply_markup=inline_kb)


async def translation_usd(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    user_data = {'tg_id': callback.message.from_user.id}
    users_response = event_service.get_users_id(user_data)
    for user in users_response:
        inline_kb = types.InlineKeyboardMarkup(row_width=1)
        inline_kb.add(types.InlineKeyboardButton("По id", callback_data="transfer_id"))
        inline_kb.add(types.InlineKeyboardButton("По nickname", callback_data="transfer_name"))
        inline_kb.add(types.InlineKeyboardButton("По номеру телефона", callback_data="transfer_number"))
        inline_kb.add(types.InlineKeyboardButton("Вернуться меню", callback_data="return_user"))
        await callback.message.answer(f"Доступно для перевода {user['balance']}\nКаким способом будете переводить: ", reply_markup=inline_kb)


async def return_user(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Главное меню: ", reply_markup=global_menu())


async def transfer_id(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(TransferState.tg_id.state)
    await callback.message.answer("Введите id получателя: ", reply_markup=user_menu_reply())


async def get_transfer_id(message: types.Message, state: FSMContext):
    if message.text == 'В меню пользователя':
        await message.answer("Меню пользователя: ", reply_markup=global_menu())
        await state.finish()
    else:
        transfer_id_num = message.text
        await state.update_data(tg_id=message.text)
        user_data = {'tg_id': message.text}
        users_response = event_service.get_users_id(user_data)
        if len(users_response) >= 1:
            await message.answer('Проверка', reply_markup=types.ReplyKeyboardRemove())
            await message.answer("Главное меню", reply_markup=global_menu())
            await state.finish()
        else:
            await message.answer("Пользователя с таким айди нету", reply_markup=types.ReplyKeyboardRemove())
            await message.answer("Меню пользователя: ", reply_markup=global_menu())
            await state.finish()


async def transfer_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Главное меню: ", reply_markup=global_menu())


async def transfer_number(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Главное меню: ", reply_markup=global_menu())


def setup(dp: Dispatcher):
    """
    ВХОД
    """
    dp.register_message_handler(get_number, state=AuthorizationState.number)
    dp.register_message_handler(get_password, state=AuthorizationState.password)

    """
    РЕГИСТРАЦИЯ
    """
    dp.register_message_handler(get_name, state=RegistrationState.name)
    dp.register_message_handler(get_phone, state=RegistrationState.phone)
    dp.register_message_handler(get_aut_password, state=RegistrationState.password)

    """
    НАЧАЛЬНОЕ МЕНЮ
    """
    dp.register_callback_query_handler(authorization, Text(contains="authorization"))
    dp.register_callback_query_handler(registration, Text(contains="registration"))
    dp.register_callback_query_handler(description, Text(contains="description"))

    """
    ГЛАВНОЕ МЕНЮ
    """
    dp.register_callback_query_handler(market, Text(equals="market"))
    dp.register_callback_query_handler(translation, Text(equals="translation"))
    dp.register_callback_query_handler(market, Text(equals="main"))
    dp.register_callback_query_handler(market, Text(equals="сhange_password"))
    dp.register_callback_query_handler(market, Text(equals="out"))
    dp.register_callback_query_handler(market, Text(equals="questions"))

    """
    ПЕРЕВОД
    """
    dp.register_callback_query_handler(translation_usd, Text(contains="usd"))
    dp.register_callback_query_handler(transfer_id, Text(contains="transfer_id"))
    dp.register_message_handler(get_transfer_id, state=TransferState.tg_id)
    dp.register_callback_query_handler(transfer_name, Text(contains="transfer_name"))
    # dp.register_message_handler(get_transfer_name, state=TransferState.name)
    dp.register_callback_query_handler(translation_usd, Text(contains="transfer_number"))
    # dp.register_message_handler(get_transfer_number, state=TransferState.number)
    dp.register_callback_query_handler(return_user, Text(contains="return_user"))
    # dp.register_callback_query_handler(translation_cryptocurrency, Text(contains="cryptocurrency"))