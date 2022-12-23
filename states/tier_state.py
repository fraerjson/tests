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
    amount = State()
    password = State()
    tg_id = State()
    choose_wallet = State()


