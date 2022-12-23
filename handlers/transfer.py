import hashlib
from handlers.home import *
from handlers.default_buttons import *
from aiogram.dispatcher import FSMContext

from services.event_playground import event_service
from states.tier_state import TransferState
from aiogram import types


async def translation(callback: types.CallbackQuery, state: FSMContext):
    id = callback.from_user.id
    user_data = {'tg_id': id}
    users_response = event_service.get_user_data_from_user_id(user_data)
    for i in users_response:
        user_data = {'users': i['id']}
    users_response = event_service.find_wallet_currency(user_data)

    await callback.message.delete()
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    for i in users_response:
        inline_kb.add(
            types.InlineKeyboardButton(f"{i}", callback_data=f"{i.lower()}")
        )
    inline_kb.add(types.InlineKeyboardButton("Вернуться меню", callback_data="return_user"))
    await callback.message.answer("С какого кошелька будете переводить?", reply_markup=inline_kb)


async def translation_usd(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(sender_currency="USD")
    await callback.message.delete()
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("По id", callback_data="transfer_id"))
    inline_kb.add(types.InlineKeyboardButton("Вернуться меню", callback_data="return_user"))
    await callback.message.answer(f"Каким способом будете переводить: ", reply_markup=inline_kb)


async def translation_btc(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(sender_currency="BTC")
    await callback.message.delete()
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("По id", callback_data="transfer_id"))
    inline_kb.add(types.InlineKeyboardButton("Вернуться меню", callback_data="return_user"))
    await callback.message.answer(f"Каким способом будете переводить: ", reply_markup=inline_kb)


async def translation_eth(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(sender_currency="ETH")
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("По id", callback_data="transfer_id"))
    inline_kb.add(types.InlineKeyboardButton("Вернуться меню", callback_data="return_user"))
    await callback.message.answer(f"Каким способом будете переводить: ", reply_markup=inline_kb)


async def translation_lit(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(sender_currency="LIT")
    await callback.message.delete()
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("По id", callback_data="transfer_id"))
    inline_kb.add(types.InlineKeyboardButton("Вернуться меню", callback_data="return_user"))
    await callback.message.answer(f"Каким способом будете переводить: ", reply_markup=inline_kb)


async def translation_bnb(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(sender_currency="BNB")
    await callback.message.delete()
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("По id", callback_data="transfer_id"))
    inline_kb.add(types.InlineKeyboardButton("Вернуться меню", callback_data="return_user"))
    await callback.message.answer(f"Каким способом будете переводить: ", reply_markup=inline_kb)


async def translation_sol(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(sender_currency="SOL")
    await callback.message.delete()
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("По id", callback_data="transfer_id"))
    inline_kb.add(types.InlineKeyboardButton("Вернуться меню", callback_data="return_user"))
    await callback.message.answer(f"Каким способом будете переводить: ", reply_markup=inline_kb)


async def transfer_id(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(TransferState.tg_id.state)
    await callback.message.answer("Введите id получателя: ", reply_markup=global_menu_reply())


async def get_transfer_id(message: types.Message, state: FSMContext):
    if message.text == 'В меню пользователя':
        await message.answer("Меню пользователя: ", reply_markup=global_menu())
        await state.finish()
    elif str(message.text) == str(message.from_user.id):
        await message.answer("Это ваш id, вы не можете переслать средства сами себе, пожалуйста введите другой id:")
    else:
        id = message.text
        user_data = {'tg_id': id}
        users_response = event_service.get_user_data_from_user_id(user_data)
        for i in users_response:
            user_data = {'users': i['id']}
        if len(users_response) >= 1:
            users_response = event_service.find_wallet_currency(user_data)
            inline_kb_rec = types.InlineKeyboardMarkup(row_width=1)
            for i in users_response:
                inline_kb_rec.add(
                    types.InlineKeyboardButton(f"{i}.", callback_data=f"rec_{i.lower()}")
                )
            inline_kb_rec.add(types.InlineKeyboardButton("Вернуться меню", callback_data="return_user"))
            await message.answer("На какой кошелек будете переводить?", reply_markup=inline_kb_rec)
            await state.finish()
        else:
            await message.answer("Пользователя с таким айди нету, пожалуйста введите коректный айди", reply_markup=types.ReplyKeyboardRemove())
            await message.answer("Меню пользователя: ", reply_markup=global_menu())
            await state.finish()




async def recipient_usd(callback: types.CallbackQuery, state: FSMContext):
    print("qweqwe")
    await state.update_data(recipient_currency="USD")
    await state.set_state(TransferState.choose_wallet)


async def recipient_btc(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(recipient_currency="BTC")
    await callback.message.delete()
    await state.set_state(TransferState.choose_wallet)


async def recipient_eth(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(recipient_currency="ETH")
    await state.set_state(TransferState.choose_wallet)


async def recipient_lit(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(recipient_currency="LIT")
    await callback.message.delete()
    await state.set_state(TransferState.choose_wallet)


async def recipient_bnb(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(recipient_currency="BNB")
    await callback.message.delete()
    await state.set_state(TransferState.choose_wallet)


async def recipient_sol(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(recipient_currency="SOL")
    await callback.message.delete()
    await state.set_state(TransferState.choose_wallet)


async def choose_wallet(message: types.Message, state: FSMContext):
    await message.answer("qweqwe")
    if message.text == 'В меню пользователя':
        await message.answer("Меню пользователя: ", reply_markup=global_menu())
        await state.finish()
    else:
        user_data = {'tg_id': message.text}
        users_response = event_service.get_user_data_from_user_id(user_data)
        if len(users_response) >= 1:
            for i in users_response:
                get_data = await state.get_data()
                await state.update_data(recipient=i['name'])
                user_data = {'currency': get_data['currency'], 'users': i['id']}

            users_response = event_service.find_wallet(user_data)
            for i in users_response:
                await state.update_data(recipient_id=i['id'])
                await state.update_data(recipient_amount=i['amount'])

        else:
            await message.answer("Пользователя с таким айди нету", reply_markup=types.ReplyKeyboardRemove())
            await message.answer("Меню пользователя: ", reply_markup=global_menu())
            await state.finish()

        user_data = {'tg_id': message.from_user.id}
        users_response = event_service.get_user_data_from_user_id(user_data)
        if len(users_response) >= 1:
            for i in users_response:
                get_data = await state.get_data()
                user_data = {'currency': get_data['currency'], 'users': i['id']}
                await state.update_data(users=i['id'])

            await state.set_state(TransferState.amount.state)
            users_response = event_service.find_wallet(user_data)
            for i in users_response:
                if i['amount'] > 0:
                    await state.update_data(amount=i['amount'])
                    await state.update_data(id=i['id'])
                    await message.answer(
                        f'Для перевода доступно {i["amount"]} USD\nВведите сумму которую хотите переслать: ')
                else:
                    await message.answer("К сожелению на вашем кошельке нету средств для перевода")
                    await state.finish()
                    await message.answer("К сожелению на этом кошельке у вас нету средств")
        else:
            await message.answer("Пользователя с таким айди нету", reply_markup=types.ReplyKeyboardRemove())
            await message.answer("Меню пользователя: ", reply_markup=global_menu())
            await state.finish()

async def get_amount(message: types.Message, state: FSMContext):
    if message.text == 'В меню пользователя':
        await message.answer("Меню пользователя: ", reply_markup=global_menu())
        await state.finish()
    else:
        balance = await state.get_data()
        try:
            qwe = int(message.text)
            if int(message.text) <= balance['amount']:
                user_data = {'tg_id': message.from_user.id}
                await state.update_data(amount_minus=message.text)
                users_response = event_service.get_user_data_from_user_id(user_data)
                for i in users_response:
                    await state.update_data(sender=i['name'])
                await state.update_data(amount=balance['amount'] - float(message.text))
                await state.update_data(recipient_amount=balance['recipient_amount'] + float(message.text))
                await state.set_state(TransferState.password.state)
                await message.answer('Для подтверждения транзакции введите пароль: ')
            else:
                await message.answer('Недостаточно средств')
                await message.answer(f'Для перевода доступно {balance["amount"]} USD\nВведите сумму которую хотите переслать: ')
        except:
            await message.answer("Введите число: ")


async def get_password_tr(message: types.Message, state: FSMContext):
    if message.text == 'В меню пользователя':
        await message.answer("Меню пользователя: ", reply_markup=global_menu())
        await state.finish()
    else:
        password = hashlib.sha256(message.text.encode())
        wallet_data = await state.get_data()
        user_data = {'password': password.hexdigest(), 'tg_id': message.from_user.id}
        users_response = event_service.check_transaction_password(user_data)
        if len(users_response) == 1:
            for i in users_response:
                valid_password = i['password']
            hash_password = hashlib.sha256(message.text.encode()).hexdigest()
            if valid_password == hash_password:
                users_response_wallet = event_service.patch_wallet(wallet_data)
                qwe = users_response_wallet['id']
                await state.update_data(wallet=qwe)
                wallet_data = await state.get_data()
                users_response_wallet = event_service.post_transactions(wallet_data)
                await message.answer("Транзакция произошла успешно!", reply_markup=types.ReplyKeyboardRemove())
                await message.answer("Меню пользователя: ", reply_markup=global_menu())
                await state.finish()
        else:
            await message.answer('Не правильный пароль, попробуйте введите еще раз: ')


async def return_user(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.delete()
    await callback.message.answer("Главное меню: ", reply_markup=global_menu())

def setup(dp: Dispatcher):
    """
    ПЕРЕВОД
    """
    dp.register_callback_query_handler(return_user, Text(equals="return_user"))
    dp.register_callback_query_handler(translation, Text(equals="translation"))
    dp.register_callback_query_handler(translation_usd, Text(contains="usd"))
    dp.register_callback_query_handler(translation_btc, Text(contains="btc"))
    dp.register_callback_query_handler(translation_eth, Text(contains="eth"))
    dp.register_callback_query_handler(translation_lit, Text(contains="lit"))
    dp.register_callback_query_handler(translation_bnb, Text(contains="bnb"))
    dp.register_callback_query_handler(translation_sol, Text(contains="sol"))

    dp.register_callback_query_handler(transfer_id, Text(contains="transfer_id"))

    dp.register_callback_query_handler(recipient_usd, Text(equals="rec_usd"))
    dp.register_callback_query_handler(recipient_btc, Text(contains="recbtc"))
    dp.register_callback_query_handler(recipient_eth, Text(contains="receth"))
    dp.register_callback_query_handler(recipient_lit, Text(contains="reclit"))
    dp.register_callback_query_handler(recipient_bnb, Text(contains="recbnb"))
    dp.register_callback_query_handler(recipient_sol, Text(contains="recsol"))

    dp.register_message_handler(get_transfer_id, state=TransferState.tg_id)
    dp.register_message_handler(choose_wallet, state=TransferState.choose_wallet)
    dp.register_message_handler(get_amount, state=TransferState.amount)
    dp.register_message_handler(get_password_tr, state=TransferState.password)
