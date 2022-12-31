import hashlib

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


from aiogram import types

from handlers.default_buttons import global_menu, global_menu_reply
from services.event_playground import event_service
from states.tier_state import WalletState


async def wallets(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    id = callback.from_user.id
    user_data = {'tg_id': id}
    users_response = event_service.get_user_data_from_user_id(user_data)
    for i in users_response:
        user_data = {'users': i['id']}
    users_response = event_service.find_wallet_currency(user_data)

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    for i in users_response:
        inline_kb.add(
            types.InlineKeyboardButton(f"{i['currency']} - {i['amount']}", callback_data=f'inf{i["currency"].lower()}')
        )
    inline_kb.add(types.InlineKeyboardButton("Добавить кошелек", callback_data="add_wallet"))
    inline_kb.add(types.InlineKeyboardButton("В меня пользователя", callback_data='return_user'))
    await callback.message.answer("Меню", reply_markup=inline_kb)


async def add_wallet(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    user_data = {'tg_id': callback.from_user.id}
    users_response = event_service.get_user_data_from_user_id(user_data)
    for i in users_response:
        user_data = {'users': i['id']}
    users_response = event_service.find_wallet_currency(user_data)

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    currency = ["USD", "BTC", "ETH", "ADA", "BNB", "XRP", "DOGE"]
    for i in users_response:
        test = i['currency']
        currency.remove(test)

    for i in currency:
        inline_kb.add(
            types.InlineKeyboardButton(f"{i}", callback_data=f'add{i.lower()}')
        )
    inline_kb.add(types.InlineKeyboardButton("В меня пользователя", callback_data='return_user'))
    await callback.message.answer('Какой хотите добавть?', reply_markup=inline_kb)


async def add_currency(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(WalletState.get_password.state)
    await state.update_data(currency=callback.data.split('add')[1].upper())
    user_data = {'tg_id': callback.from_user.id}
    users_response = event_service.get_user_data_from_user_id(user_data)
    await state.update_data(amount=0)
    for i in users_response:
        user_data = {'users': i['id']}
        await state.update_data(users=i['id'])
    await callback.message.answer("Для обавления кошелька введите пароль: ")


async def get_password_for_wallet(message: types.Message, state: FSMContext):
    password = hashlib.sha256(message.text.encode())
    await message.delete()
    user_data = {'password': password.hexdigest(), 'tg_id': message.from_user.id}
    users_response = event_service.check_transaction_password(user_data)
    if len(users_response) == 1:
        wallet_data = await state.get_data()
        users_response = event_service.add_wallet(wallet_data)
        await message.answer('Кошелек котов к работе!')
        await message.answer("Меню пользователя: ", reply_markup=global_menu())
        await state.finish()
    else:
        await message.answer('Не верный пароль. Повторите попытку: ')


async def inf_wallet(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(WalletState.inf_wallet.state)
    await state.update_data(currency=callback.data.split('inf')[1].upper())
    user_data = {'tg_id': callback.from_user.id}
    users_response = event_service.get_user_data_from_user_id(user_data)
    for i in users_response:
        await state.update_data(users=i['id'])
        name = i['name']
    wallet_data = await state.get_data()
    users_response = event_service.find_wallet(wallet_data)
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Удалить Кошелек", callback_data=f'delete_wallet_{wallet_data["currency"]}'))
    inline_kb.add(types.InlineKeyboardButton("В меня пользователя", callback_data='return_user'))
    await state.finish()
    for i in users_response:
        await state.update_data(wallet_id=i['id'])
        await state.update_data(wallet_amount=i['amount'])
        await state.update_data(wallet_currency=i['currency'])
        await callback.message.answer(f"currency - {i['currency']}\namount - {i['amount']}\nuser - {name}", reply_markup=inline_kb)


async def delete_wallet(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(WalletState.inf_wallet)
    data = await state.get_data()
    if data['wallet_amount'] > 0:
        await callback.message.answer(f"У вас на балансе осталось {data['wallet_amount']} {data['wallet_currency']} если вы удалите кошелек то все стредства пропадут.")
    await state.set_state(WalletState.get_password_delete)
    await callback.message.answer("Для удаления кошелька введите пароль: ", reply_markup=global_menu_reply())


async def get_password_for_delete_wallet(message: types.Message, state: FSMContext):
    if message.text == 'В меню пользователя':
        await message.answer("Меню пользователя: ", reply_markup=global_menu())
        await state.finish()
    else:
        password = hashlib.sha256(message.text.encode())
        await message.delete()
        user_data = {'password': password.hexdigest(), 'tg_id': message.from_user.id}
        users_response = event_service.check_transaction_password(user_data)
        if len(users_response) == 1:
            wallet_data = await state.get_data()
            users_response = event_service.delete_wallet(wallet_data)
            await message.answer('Кошелек удален')
            await message.answer("Меню пользователя: ", reply_markup=global_menu())
            await state.finish()
        else:
            await message.answer('Не верный пароль. Повторите попытку: ')


async def return_user(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.delete()
    await callback.message.answer("Главное меню: ", reply_markup=global_menu())


def setup(dp: Dispatcher):
    """
    МОИ КОШЕЛЬКИ
    """
    dp.register_callback_query_handler(return_user, Text(contains="return_user"))

    dp.register_callback_query_handler(delete_wallet, Text(contains="delete_wallet_USD"))
    dp.register_callback_query_handler(delete_wallet, Text(contains="delete_wallet_BTC"))
    dp.register_callback_query_handler(delete_wallet, Text(contains="delete_wallet_ETH"))
    dp.register_callback_query_handler(delete_wallet, Text(contains="delete_wallet_ADA"))
    dp.register_callback_query_handler(delete_wallet, Text(contains="delete_wallet_BNB"))
    dp.register_callback_query_handler(delete_wallet, Text(contains="delete_wallet_XRP"))
    dp.register_callback_query_handler(delete_wallet, Text(contains="delete_wallet_DOGE"))

    dp.register_callback_query_handler(wallets, Text(contains="wallets"))
    dp.register_callback_query_handler(add_wallet, Text(contains="add_wallet"))
    dp.register_callback_query_handler(add_currency, Text(contains="addusd"))
    dp.register_callback_query_handler(add_currency, Text(contains="addbtc"))
    dp.register_callback_query_handler(add_currency, Text(contains="addeth"))
    dp.register_callback_query_handler(add_currency, Text(contains="addada"))
    dp.register_callback_query_handler(add_currency, Text(contains="addbnb"))
    dp.register_callback_query_handler(add_currency, Text(contains="addxrp"))
    dp.register_callback_query_handler(add_currency, Text(contains="adddoge"))

    dp.register_callback_query_handler(inf_wallet, Text(contains="infusd"))
    dp.register_callback_query_handler(inf_wallet, Text(contains="infbtc"))
    dp.register_callback_query_handler(inf_wallet, Text(contains="infeth"))
    dp.register_callback_query_handler(inf_wallet, Text(contains="infada"))
    dp.register_callback_query_handler(inf_wallet, Text(contains="infbnb"))
    dp.register_callback_query_handler(inf_wallet, Text(contains="infxrp"))
    dp.register_callback_query_handler(inf_wallet, Text(contains="infdoge"))

    dp.register_message_handler(get_password_for_wallet, state=WalletState.get_password)
    dp.register_message_handler(get_password_for_delete_wallet, state=WalletState.get_password_delete)







