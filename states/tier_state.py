from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationState(StatesGroup):
    fio = State()
    phone = State()
    email = State()
    title_company = State()
    revenue = State()


class AuthorizationState(StatesGroup):
    number = State()
    password = State()



class MenuState(StatesGroup):
    menu = State()
