import hashlib
from handlers.home import *
from handlers.default_buttons import *
from aiogram.dispatcher import FSMContext

from services.event_playground import event_service
from states.tier_state import TransferState
from aiogram import types

global_currency ={
    'USD': 1,
    'BTC': 16845,
    'ETH': 1220,
    'BNB': 243,
    'XRP': 0.35,
    'DOGE': 0.07,
    'ADA': 0.26,
}

async def translation(callback: types.CallbackQuery, state: FSMContext):
    id = callback.from_user.id
    user_data = {'tg_id': id}
    users_response = event_service.get_user_data_from_user_id(user_data)
    await state.update_data(sender_tg_id=id)
    for i in users_response:
        user_data = {'users': i['id']}
        await state.update_data(sender_id=i['id'])
        await state.update_data(sender=i['name'])
    users_response = event_service.find_wallet_currency(user_data)

    await callback.message.delete()
    inline_kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    for i in users_response:
        inline_kb.add(
            types.KeyboardButton(f"{i['currency']}")
        )
    inline_kb.add(types.KeyboardButton("В меню пользователя"))
    await callback.message.answer("С какого кошелька будете переводить?", reply_markup=inline_kb)
    await state.set_state(TransferState.sender_currency)

async def sender_currency(message: types.Message, state: FSMContext):
    recipient_currency = message.text
    if recipient_currency == "В меню пользователя":
        await state.finish()
        await message.answer("Транзакция прервана", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Меню пользователя", reply_markup=global_menu())

    elif recipient_currency == "USD":
        await state.update_data(sender_currency="USD")
        await state.set_state(TransferState.tg_id.state)
        await message.answer("Введите айди получателя:", reply_markup=first_menu_reply())
    elif recipient_currency == "BTC":
        await state.update_data(sender_currency="BTC")
        await state.set_state(TransferState.tg_id.state)
        await message.answer("Введите айди получателя:", reply_markup=first_menu_reply())
    elif recipient_currency == "ETH":
        await state.update_data(sender_currency="ETH")
        await state.set_state(TransferState.tg_id.state)
        await message.answer("Введите айди получателя:", reply_markup=first_menu_reply())
    elif recipient_currency == "ADA":
        await state.update_data(sender_currency="ADA")
        await state.set_state(TransferState.tg_id.state)
        await message.answer("Введите айди получателя:", reply_markup=first_menu_reply())
    elif recipient_currency == "BNB":
        await state.update_data(sender_currency="BNB")
        await state.set_state(TransferState.tg_id.state)
        await message.answer("Введите айди получателя:", reply_markup=first_menu_reply())
    elif recipient_currency == "XRP":
        await state.update_data(sender_currency="XRP")
        await state.set_state(TransferState.tg_id.state)
        await message.answer("Введите айди получателя:", reply_markup=first_menu_reply())
    elif recipient_currency == "DOGE":
        await state.update_data(sender_currency="DOGE")
        await state.set_state(TransferState.tg_id.state)
        await message.answer("Введите айди получателя:", reply_markup=first_menu_reply())
    else:
        await message.answer("Такого варианта ответа нету")

async def get_transfer_id(message: types.Message, state: FSMContext):
    if message.text == 'В меню пользователя':
        await message.answer("Меню пользователя: ", reply_markup=global_menu())
        await state.finish()
    else:
        id = message.text
        await state.update_data(sender_tg_id=id)
        recipient_data = {'tg_id': id}
        users_response = event_service.get_user_data_from_user_id(recipient_data)
        for i in users_response:
            user_data = {'users': i['id']}
            await state.update_data(recipient_id=i['id'])
            await state.update_data(recipient=i['name'])
        if len(users_response) >= 1:
            users_response = event_service.find_wallet_currency(user_data)
            reply_kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            for i in users_response:
                reply_kb.add(KeyboardButton(f'{i["currency"]}'))
            reply_kb.add(KeyboardButton("В меню пользователя"))
            await message.answer("На какой кошелек будете переводить?", reply_markup=reply_kb)
            get_data = await state.get_data()
            user_data = {'currency': get_data['sender_currency'], 'users': get_data['sender_id']}
            sender_response = event_service.find_wallet(user_data)
            for i in sender_response:
                await state.update_data(sender_wallet_id=i['id'])
                await state.update_data(sender_amount=i['amount'])
            await state.set_state(TransferState.choose_wallet.state)
        else:
            await message.answer("Пользователя с таким айди нету, пожалуйста введите коректный айди: ", reply_markup=first_menu_reply())


async def recipient_currency(message: types.Message, state: FSMContext):
    recipient_currency = message.text
    if recipient_currency == "В меню пользователя":
        await state.finish()
        await message.answer("Транзакция прервана", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Меню пользователя", reply_markup=global_menu())

    elif recipient_currency == "USD":
        await state.set_state(TransferState.amount.state)
        await state.update_data(recipient_currency="USD")
        get_data = await state.get_data()
        await message.answer(
            f"Сколько вы хотите перевести?\nУ вас на балансе {get_data['sender_amount']} {get_data['sender_currency']}",
            reply_markup=amount_reply()
        )
        user_data = {'currency': get_data['recipient_currency'], 'users': get_data['recipient_id']}
        recipient_response = event_service.find_wallet(user_data)
        for i in recipient_response:
            await state.update_data(recipient_wallet_id=i['id'])
            await state.update_data(recipient_amount=i['amount'])
    elif recipient_currency == "BTC":
        await state.set_state(TransferState.amount.state)
        await state.update_data(recipient_currency="BTC")
        get_data = await state.get_data()
        await message.answer(
            f"Сколько вы хотите перевести?\nУ вас на балансе {get_data['sender_amount']} {get_data['sender_currency']}",
            reply_markup=amount_reply())
        user_data = {'currency': get_data['recipient_currency'], 'users': get_data['recipient_id']}
        recipient_response = event_service.find_wallet(user_data)
        for i in recipient_response:
            await state.update_data(recipient_wallet_id=i['id'])
            await state.update_data(recipient_amount=i['amount'])
    elif recipient_currency == "ETH":
        await state.set_state(TransferState.amount.state)
        await state.update_data(recipient_currency="ETH")
        get_data = await state.get_data()
        await message.answer(
            f"Сколько вы хотите перевести?\nУ вас на балансе {get_data['sender_amount']} {get_data['sender_currency']}",
            reply_markup=amount_reply())
        user_data = {'currency': get_data['recipient_currency'], 'users': get_data['recipient_id']}
        recipient_response = event_service.find_wallet(user_data)
        for i in recipient_response:
            await state.update_data(recipient_wallet_id=i['id'])
            await state.update_data(recipient_amount=i['amount'])
    elif recipient_currency == "ADA":
        await state.set_state(TransferState.amount.state)
        await state.update_data(recipient_currency="ADA")
        get_data = await state.get_data()
        await message.answer(
            f"Сколько вы хотите перевести?\nУ вас на балансе {get_data['sender_amount']} {get_data['sender_currency']}",
            reply_markup=amount_reply())
        user_data = {'currency': get_data['recipient_currency'], 'users': get_data['recipient_id']}
        recipient_response = event_service.find_wallet(user_data)
        for i in recipient_response:
            await state.update_data(recipient_wallet_id=i['id'])
            await state.update_data(recipient_amount=i['amount'])
    elif recipient_currency == "BNB":
        await state.set_state(TransferState.amount.state)
        await state.update_data(recipient_currency="BNB")
        get_data = await state.get_data()
        await message.answer(
            f"Сколько вы хотите перевести?\nУ вас на балансе {get_data['sender_amount']} {get_data['sender_currency']}",
            reply_markup=amount_reply())
        user_data = {'currency': get_data['recipient_currency'], 'users': get_data['recipient_id']}
        recipient_response = event_service.find_wallet(user_data)
        for i in recipient_response:
            await state.update_data(recipient_wallet_id=i['id'])
            await state.update_data(recipient_amount=i['amount'])
    elif recipient_currency == "DOGE":
        await state.set_state(TransferState.amount.state)
        await state.update_data(recipient_currency="XRP")
        get_data = await state.get_data()
        await message.answer(
            f"Сколько вы хотите перевести?\nУ вас на балансе {get_data['sender_amount']} {get_data['sender_currency']}",
            reply_markup=amount_reply())
        user_data = {'currency': get_data['recipient_currency'], 'users': get_data['recipient_id']}
        recipient_response = event_service.find_wallet(user_data)
        for i in recipient_response:
            await state.update_data(recipient_wallet_id=i['id'])
            await state.update_data(recipient_amount=i['amount'])
    elif recipient_currency == "DOGE":
        await state.set_state(TransferState.amount.state)
        await state.update_data(recipient_currency="DOGE")
        get_data = await state.get_data()
        await message.answer(
            f"Сколько вы хотите перевести?\nУ вас на балансе {get_data['sender_amount']} {get_data['sender_currency']}",
            reply_markup=amount_reply())
        user_data = {'currency': get_data['recipient_currency'], 'users': get_data['recipient_id']}
        recipient_response = event_service.find_wallet(user_data)
        for i in recipient_response:
            await state.update_data(recipient_wallet_id=i['id'])
            await state.update_data(recipient_amount=i['amount'])
    else:
        await message.answer("Такого варианта ответа нету")


async def get_amount(message: types.Message, state: FSMContext):
    get_data = await state.get_data()
    if message.text == 'В меню пользователя':
        await message.answer("Меню пользователя: ", reply_markup=global_menu())
        await state.finish()
    elif message.text == '25%':
        send_amount = get_data['sender_amount'] * 0.25
        await state.update_data(new_recipient_amount=get_data['recipient_amount'] + send_amount)
        await state.update_data(new_sender_amount=float("{0:.3f}".format(get_data['sender_amount'] - send_amount)))
        await state.update_data(send_amount=send_amount)
        await state.set_state(TransferState.password.state)
        await message.answer('Для подтверждения транзакции введите пароль: ')
    elif message.text == '50%':
        send_amount = get_data['sender_amount'] * 0.50
        await state.update_data(new_recipient_amount=get_data['recipient_amount'] + send_amount)
        await state.update_data(new_sender_amount=float("{0:.3f}".format(get_data['sender_amount'] - send_amount)))
        await state.update_data(send_amount=send_amount)
        await state.set_state(TransferState.password.state)
        await message.answer('Для подтверждения транзакции введите пароль: ')
    elif message.text == '75%':
        send_amount = get_data['sender_amount'] * 0.75
        await state.update_data(new_recipient_amount=get_data['recipient_amount'] + send_amount)
        await state.update_data(new_sender_amount=float("{0:.3f}".format(get_data['sender_amount'] - send_amount)))
        await state.update_data(send_amount=send_amount)
        await state.set_state(TransferState.password.state)
        await message.answer('Для подтверждения транзакции введите пароль: ')
    elif message.text == 'Всё':
        send_amount = get_data['sender_amount']
        await state.update_data(new_recipient_amount=get_data['recipient_amount'] + send_amount)
        await state.update_data(new_sender_amount=float("{0:.3f}".format(get_data['sender_amount'] - send_amount)))
        await state.update_data(send_amount=send_amount)
        await state.set_state(TransferState.password.state)
        await message.answer('Для подтверждения транзакции введите пароль: ')
    else:
        try:
            send_amount = float(message.text)
            if float(message.text) <= get_data['sender_amount']:
                await state.update_data(new_recipient_amount=get_data['recipient_amount'] + send_amount)
                await state.update_data(new_sender_amount=float("{0:.3f}".format(get_data['sender_amount'] - send_amount)))
                await state.update_data(send_amount=send_amount)
                await state.set_state(TransferState.password.state)
                await message.answer('Для подтверждения транзакции введите пароль: ')


            else:
                await message.answer('Недостаточно средств')
                await message.answer(f'Для перевода доступно {get_data["sender_amount"]} {get_data["sender_currency"] }\nВведите сумму которую хотите переслать: ')
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
                sender_tier = i['tier']
            hash_password = hashlib.sha256(message.text.encode()).hexdigest()
            if valid_password == hash_password:
                get_data = await state.get_data()
                usd_recipient = global_currency[f'{get_data["sender_currency"]}'] * get_data['send_amount']
                if sender_tier == "U":
                    commission = usd_recipient * 0.1
                    await state.update_data(commission=float("{0:.4f}".format(commission)))
                    usd_recipient = usd_recipient * 0.90
                elif sender_tier == "B":
                    commission = usd_recipient * 0.07
                    await state.update_data(commission=float("{0:.4f}".format(commission)))
                    usd_recipient = usd_recipient * 0.93
                elif sender_tier == "S":
                    commission = usd_recipient * 0.05
                    await state.update_data(commission=float("{0:.4f}".format(commission)))
                    usd_recipient = usd_recipient * 0.95
                elif sender_tier == "G":
                    commission = usd_recipient * 0.03
                    await state.update_data(commission=float("{0:.4f}".format(commission)))
                    usd_recipient = usd_recipient * 0.97
                elif sender_tier == "A":
                    commission = 0
                    await state.update_data(commission=commission)
                await state.update_data(received_amount=float("{0:.4f}".format(usd_recipient - commission)))
                res_currency_amount = global_currency[f'{get_data["recipient_currency"]}']
                new_recipient_amount = usd_recipient / res_currency_amount
                new_recipient_amount = new_recipient_amount + get_data['recipient_amount']
                await state.update_data(new_recipient_amount=float("{0:.4f}".format(new_recipient_amount)))
                users_response_wallet = event_service.patch_wallet(wallet_data)
                wallet_data = await state.get_data()
                users_response_wallet = event_service.patch_wallet(wallet_data)
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
    # dp.register_callback_query_handler(translation,
    #                                    Text(equals="translation") or
    #                                    Text(equals="transaction_history") or
    #                                    Text(equals="main")
    #                                    )
    dp.register_callback_query_handler(translation, Text(equals="translation"))
    dp.register_callback_query_handler(translation, Text(equals="transaction_history"))
    dp.register_callback_query_handler(translation, Text(equals="main"))



    dp.register_message_handler(sender_currency, state=TransferState.sender_currency)
    dp.register_message_handler(get_transfer_id, state=TransferState.tg_id)
    dp.register_message_handler(recipient_currency, state=TransferState.choose_wallet)
    dp.register_message_handler(get_amount, state=TransferState.amount)
    dp.register_message_handler(get_password_tr, state=TransferState.password)
