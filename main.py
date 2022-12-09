import logging

from aiogram import Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.users import setup as user_handler_setup
from services.event_playground import event_service
from bot_creation import bot


logging.basicConfig(level=logging.INFO)

dp = Dispatcher(bot, storage=MemoryStorage())


async def startup(_):
    event_service.check_availability()


@dp.message_handler(commands=["start"])
async def get_admin_commands(msg: types.Message):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Вход", callback_data="authorization"))
    inline_kb.add(types.InlineKeyboardButton("Регистрация", callback_data="registration"))
    inline_kb.add(types.InlineKeyboardButton("Описание", callback_data="description"))
    try:
        await msg.edit_text("Choose admin action", reply_markup=inline_kb)
    except:
        await msg.reply("Choose admin action", reply_markup=inline_kb)


@dp.callback_query_handler(Text(contains="market"))
async def market(callback: types.CallbackQuery, state: FSMContext):
    print("qwe")
    await callback.message.answer("Тут нихуя нету, иди нахуй")


@dp.callback_query_handler(Text(contains="return"), state="*")
async def return_handler(callback: types.CallbackQuery, state: FSMContext):
    await get_admin_commands(callback.message)
    await state.finish()


user_handler_setup(dp)
executor.start_polling(dp, skip_updates=True, on_startup=startup)