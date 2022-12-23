from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


from aiogram import types


async def wallets(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    menu_kb = types.InlineKeyboardMarkup(row_width=1)
    menu_kb.add(types.InlineKeyboardButton("Мои кошельки", callback_data="my_wallets"))
    menu_kb.add(types.InlineKeyboardButton("Добавить кошелек", callback_data="out"))
    await callback.message.answer("Меню", reply_markup=menu_kb)


async def my_wallets(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    menu_kb = types.InlineKeyboardMarkup(row_width=1)
    menu_kb.add(types.InlineKeyboardButton("Мои кошельки", callback_data="my_wallets"))
    menu_kb.add(types.InlineKeyboardButton("Добавить кошелек", callback_data="out"))
    await callback.message.answer("Меню", reply_markup=menu_kb)

def setup(dp: Dispatcher):
    """
    МОИ КОШЕЛЬКИ
    """
    dp.register_callback_query_handler(wallets, Text(contains="wallets"))
    dp.register_callback_query_handler(my_wallets, Text(contains="my_wallets"))


