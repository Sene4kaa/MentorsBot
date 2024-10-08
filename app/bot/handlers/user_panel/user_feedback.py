import gspread

import datetime

import psycopg
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from django.conf import settings

from bot.services.keyboards import get_user_list_kb, get_back_to_user_menu_kb, get_3_points_kb
from bot.services.messages import get_lessons_with_user_id

DATABASE_URL = settings.DATABASE_URL


class Feedback(StatesGroup):
    first_question = State()
    second_question = State()
    third_question = State()
    final_question = State()


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list) + 1)


gc = gspread.service_account(filename="test.json")
sh = gc.open_by_key(settings.SAMPLE_SPREADSHEET_ID)
worksheet_lesson = sh.worksheet("Lessons")


router = Router()

reasons = ["Формат", "Содержание", "Подача", "Задания", "Взаимодействие с преподавателем"]


@router.callback_query(StateFilter(None), F.data == "Feedback")
async def feedback_line_started(callback: CallbackQuery, state: FSMContext):

    lessons_list = get_lessons_with_user_id(callback.from_user.id)

    if len(lessons_list) == 0:

        await state.clear()
        await callback.message.edit_text(
            text="Ты не записан(а) <i>ни на одно</i> занятие 😥", reply_markup=get_back_to_user_menu_kb()
        )
    else:
        await callback.message.edit_text(
            text="На какое занятие вы бы хотели оставить отзыв?", reply_markup=get_user_list_kb(lessons_list)
        )

        await state.set_state(Feedback.first_question)


@router.callback_query(Feedback.first_question)
async def first_question_feedback(callback: CallbackQuery, state: FSMContext):

    await state.update_data(lesson=callback.data)

    await callback.message.edit_text(
        text=f"Отзыв на <b>{callback.data}</b>\n\nКак вы оцениваете занятие?", reply_markup=get_3_points_kb()
    )

    await state.set_state(Feedback.second_question)


@router.callback_query(Feedback.second_question)
async def second_question_feedback(callback: CallbackQuery, state: FSMContext):

    await state.update_data(grade=callback.data)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Отзыв на <b>{user_data['lesson']}</b>\n\nЧто в занятии понравилось больше всего?",
        reply_markup=get_user_list_kb(reasons),
    )

    await state.set_state(Feedback.third_question)


@router.callback_query(Feedback.third_question)
async def third_question_feedback(callback: CallbackQuery, state: FSMContext):

    await state.update_data(liked=callback.data)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Отзыв на <b>{user_data['lesson']}</b>\n\nОпишите общее впечатление",
    )

    await state.set_state(Feedback.final_question)


@router.message(Feedback.final_question)
async def final_question_feedback(message: Message, state: FSMContext):

    await state.update_data(overall_impression=message.text)
    user_data = await state.get_data()

    next_row_id = str(int(next_available_row(worksheet_lesson)) + 1)
    now = datetime.datetime.now().strftime("%d-%m-%Y")

    worksheet_lesson.update_acell(f"A{next_row_id}", now)
    worksheet_lesson.update_acell(f"B{next_row_id}", user_data["lesson"])
    worksheet_lesson.update_acell(f"C{next_row_id}", user_data["grade"])
    worksheet_lesson.update_acell(f"D{next_row_id}", user_data["liked"])
    worksheet_lesson.update_acell(f"E{next_row_id}", user_data["overall_impression"])

    await message.delete()

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            bot_messages = cursor.execute(
                "SELECT * FROM last_bot_message WHERE user_id=%s", [message.from_user.id]
            ).fetchall()

            cursor.execute("""DELETE FROM last_bot_message WHERE user_id=%s""", [message.from_user.id])
            conn.commit()

    for bot_message in bot_messages:
        try:
            await message.bot.delete_message(
                chat_id=message.from_user.id,
                message_id=bot_message[1]
            )
        finally:
            continue

    await message.answer(
        text="Благодарим за отзыв!\nВаше мнение действительно важно для нас ❤️",
        reply_markup=get_back_to_user_menu_kb(),
    )

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""INSERT INTO last_bot_message VALUES (%s, %s)""",
                           [message.from_user.id, message.message_id - 1])
            conn.commit()

    await state.clear()
