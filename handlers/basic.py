from handlers.home import *
from handlers.default_buttons import *
from aiogram.dispatcher import FSMContext

from services.event_playground import event_service
from states.tier_state import TransferState
from aiogram import types


async def main(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Что вас интерсует?", reply_markup=main_button())

async def out(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Для выхода из учетной записи вам требуется ввести пароль.\nВведите пароль: ", reply_markup=global_menu_reply())

async def out_password(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в меню':
        await message.answer("Choose admin action", reply_markup=first_menu())
        await state.finish()
    else:
        password = message.text
        user_data = {'tg_id': message.from_user.id}
        users_response = event_service.get_user_data_from_user_id(user_data)
        for i in users_response:
            correct_password = i['password']
        if password == correct_password:
            await message.answer("Вы вышли из учетной записи. До скорых встреч")
            await state.finish()
            await message.answer("Choose admin action", reply_markup=first_menu())
        else:
            await message.answer("Не верный пароль. \nПожалуйста введите коректный пароль:")

def setup(dp: Dispatcher):
    """
    ОСНОВНЫЕ
    """
    # dp.register_callback_query_handler(market, Text(equals="сhange_password"))
    dp.register_callback_query_handler(out, Text(equals="out"))
    dp.register_message_handler(out_password, state=OutState.password)
