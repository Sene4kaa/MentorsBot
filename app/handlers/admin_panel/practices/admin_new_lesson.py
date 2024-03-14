import psycopg
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter

from config import DATABASE_URL
from services.keyboards import get_back_to_admin_menu_kb, delete_admin_practice_kb


class NewLesson(StatesGroup):
    entering_lesson = State()
    accepting_lesson = State()


router = Router()


@router.callback_query(StateFilter(None), F.data == "AddLesson")
async def start_adding_lesson(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Введите название предмета")

    await state.set_state(NewLesson.entering_lesson)


@router.message(NewLesson.entering_lesson)
async def lesson_entered(message: Message, state: FSMContext):

    answer = message.text
    await message.delete()
    await state.update_data(entered_lesson=answer)

    await message.answer(text=f"Вы ввели {answer}", reply_markup=delete_admin_practice_kb())

    await state.set_state(NewLesson.accepting_lesson)


@router.callback_query(NewLesson.accepting_lesson)
async def accepting_lesson(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    sql = """INSERT INTO lessons_title (title) VALUES (%s)"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, [user_data["entered_lesson"]])
            conn.commit()

    await callback.message.edit_text(text="Предмет успешно добавлен!", reply_markup=get_back_to_admin_menu_kb())

    await state.clear()
