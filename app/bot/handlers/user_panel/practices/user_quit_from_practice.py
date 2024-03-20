import gspread
import psycopg

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from django.conf import settings

from bot.services.messages import get_lessons_with_user_id
from bot.services.keyboards import (
    get_user_accepting_quit_kb,
    get_back_to_user_menu_kb,
    get_user_cancel_quit_practice_kb,
    get_user_cancel_quit_kb,
)

DATABASE_URL = settings.DATABASE_URL


class QuitingPractice(StatesGroup):
    choosing_practice = State()
    choosing_reason = State()
    accepting = State()


router = Router()

gc = gspread.service_account(filename="test.json")
sh = gc.open_by_key(settings.SAMPLE_SPREADSHEET_ID)
worksheet_sign_up = sh.worksheet("SignUpPractices")

reasons = ["Накладка в расписании", "Не успеваю", "Перезапишусь на другое время"]


@router.callback_query(StateFilter(None), F.data == "QuitFromPractice")
async def start_quiting_from_practice(callback: CallbackQuery, state: FSMContext):

    practices = get_lessons_with_user_id(callback.from_user.id)
    if len(practices) == 0:
        await callback.message.edit_text(
            text="Ты не записан(а) <i>ни на одно</i> занятие 😥", reply_markup=get_user_cancel_quit_kb(practices)
        )
    else:
        await callback.message.edit_text(
            text="Выбери занятие, от которого хочешь отписаться 👀", reply_markup=get_user_cancel_quit_kb(practices)
        )

        await state.set_state(QuitingPractice.choosing_practice)


@router.callback_query(F.data == "CancelToChoosingPracticeForQuitOperation")
async def start_quiting_from_practice(callback: CallbackQuery, state: FSMContext):

    practices = get_lessons_with_user_id(callback.from_user.id)
    await callback.message.edit_text(
        text="Выбери занятие, от которого хочешь отписаться 👀", reply_markup=get_user_cancel_quit_kb(practices)
    )

    await state.set_state(QuitingPractice.choosing_practice)


@router.callback_query(F.data == "CancelToChoosingReasonForQuitOperation")
async def practice_chosen(callback: CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    await callback.message.edit_text(
        text=f"Ты хочешь отписаться от предмета <b>{user_data['chosen_practice']}</b>.\n\nВыбери, пожалуйста, причину отмены записи ✍️",
        reply_markup=get_user_cancel_quit_practice_kb(reasons),
    )

    await state.set_state(QuitingPractice.choosing_reason)


@router.callback_query(QuitingPractice.choosing_practice)
async def practice_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_practice=callback.data)

    await callback.message.edit_text(
        text=f"Вы хотите отписаться от предмета <b>{callback.data}</b>.\n\nВыбери, пожалуйста, причину отмены записи ✍️",
        reply_markup=get_user_cancel_quit_practice_kb(reasons),
    )

    await state.set_state(QuitingPractice.choosing_reason)


@router.callback_query(QuitingPractice.choosing_reason)
async def reason_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_reason=callback.data)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Вы хотите отписаться от предмета\n<b>{user_data['chosen_practice']}</b>\n\nПричина: {user_data['chosen_reason']}\n\n"
        + "<u>Подтверди отмену записи</u>",
        reply_markup=get_user_accepting_quit_kb(),
    )
    await state.set_state(QuitingPractice.accepting)


@router.callback_query(QuitingPractice.accepting)
async def successful(callback: CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    sql_quit_reason = """INSERT INTO quited_practice (practice, reason) VALUES (%s, %s)"""
    sql_practice = """DELETE FROM practices WHERE lessons=%s AND user_id=%s"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_quit_reason, [user_data["chosen_practice"], user_data["chosen_reason"]])
            cursor.execute(sql_practice, [user_data["chosen_practice"], callback.from_user.id])

            if callback.from_user.id == 5444762353:
                user_name = cursor.execute(
                    "SELECT surname, name FROM users WHERE user_id=%s", [544476235]
                ).fetchall()
            else:
                user_name = cursor.execute(
                    "SELECT surname, name FROM users WHERE user_id=%s", [callback.from_user.id]
                ).fetchall()

            conn.commit()

    res = [
        i + 1
        for i, r in enumerate(worksheet_sign_up.get_all_values())
        if r[0] == user_data["chosen_practice"] and r[1] == user_name[0][0] and r[2] == user_name[0][1]
    ]
    if res:
        worksheet_sign_up.delete_rows(res[0])

    await callback.message.edit_text(
        text=f"Вы успешно отписались от занятия <b>{user_data['chosen_practice']}</b>!",
        reply_markup=get_back_to_user_menu_kb(),
    )
    await state.clear()
