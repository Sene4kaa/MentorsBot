import psycopg
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter

from config import DATABASE_URL
from services.keyboards import get_back_to_admin_menu_kb, delete_admin_practice_kb


class NewWorkshop(StatesGroup):
    entering_workshop = State()
    accepting_workshop = State()


router = Router()

last_bot_message_id = 0


@router.callback_query(StateFilter(None), F.data == "AddWorkshop")
async def start_adding_workshop(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text(text="Введите название предмета")

    await state.set_state(NewWorkshop.entering_workshop)


@router.message(NewWorkshop.entering_workshop)
async def workshop_entered(message: Message, state: FSMContext):

    answer = message.text
    await message.delete()
    await state.update_data(entered_workshop=answer)

    await message.answer(
        message=last_bot_message_id, text=f"Вы ввели {answer}", reply_markup=delete_admin_practice_kb()
    )

    await state.set_state(NewWorkshop.accepting_workshop)


@router.callback_query(NewWorkshop.accepting_workshop)
async def accepting_workshop(callback: CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    sql = """INSERT INTO workshops_title (title) VALUES (%s)"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, [user_data["entered_workshop"]])
            conn.commit()

    await callback.message.edit_text(text="Предмет успешно добавлен!", reply_markup=get_back_to_admin_menu_kb())

    await state.clear()
