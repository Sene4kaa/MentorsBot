import asyncio

import psycopg
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from django.conf import settings

from bot.services.keyboards import get_admin_list_kb, get_back_to_admin_menu_kb, get_back_to_user_menu_kb

DATABASE_URL = settings.DATABASE_URL


class AdminMessage(StatesGroup):
    writing_message = State()
    accepting = State()


router = Router()


@router.callback_query(F.data == "SendAdminToUsers")
async def admin_write_message(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Напишите сообщение.\nЧтобы сделать текст жирным перед началом поставьте [b], а в конце [/b] Пример: [b]Этот текст будет жирным[/b]\n\n"
        + "Аналогично: [i]текст[/i] - курсив, [u]текст[/u] - подчеркнутый\n<b>Вместо [ и ] нужно использовать знаки меньше и больше соответственно</b>."
    )
    await state.set_state(AdminMessage.writing_message)


@router.message(AdminMessage.writing_message)
async def message_writen(message: Message, state: FSMContext):

    answer = "Вы хотите отправить такое сообщение?\n\n" + message.text
    await state.update_data(msg=message.text)

    await message.answer(text=answer, reply_markup=get_admin_list_kb(["Подтвердить"]))
    await state.set_state(AdminMessage.accepting)


@router.callback_query(AdminMessage.accepting)
async def sending_message(callback: CallbackQuery, state: FSMContext, bot: Bot):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            users = cursor.execute("""SELECT chat_id FROM users""").fetchall()
            conn.commit()
    admin_data = await state.get_data()

    for user in users:
        await bot.send_message(chat_id=user[0], text=admin_data["msg"], reply_markup=get_back_to_user_menu_kb())
        await asyncio.sleep(0.033)

    await callback.message.edit_text(
        text="Сообщение отправлено всем пользователям!", reply_markup=get_back_to_admin_menu_kb()
    )
    await state.clear()
