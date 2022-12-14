from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationState(StatesGroup):
    name = State()
    phone = State()
    password = State()


class AuthorizationState(StatesGroup):
    name = State()
    number = State()
    password = State()


class MenuState(StatesGroup):
    menu = State()


class TransferState(StatesGroup):
    transfer = State()
    name = State()
    tg_id = State()
    number = State()


