from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationState(StatesGroup):
    name = State()
    phone = State()
    password = State()


class AuthorizationState(StatesGroup):
    name = State()
    number = State()
    password = State()


class OutState(StatesGroup):
    menu = State()
    password = State()


class TransferState(StatesGroup):
    transfer = State()
    sender_currency = State()
    amount = State()
    password = State()
    tg_id = State()
    choose_wallet = State()
    choose_amount = State()


class WalletState(StatesGroup):
    amount_wallets = State()
    add_wallet = State()
    get_password = State()
    inf_wallet = State()
    get_password_delete = State()

