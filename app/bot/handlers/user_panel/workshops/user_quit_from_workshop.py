import gspread
import psycopg

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from django.conf import settings

from bot.services.keyboards import get_user_accept_kb, get_back_to_user_menu_kb, get_user_list_kb

DATABASE_URL = settings.DATABASE_URL


class QuitWorkshop(StatesGroup):
    accepting_quit = State()
    choosing_reason = State()


router = Router()

gc = gspread.service_account(filename="test.json")
sh = gc.open_by_key(settings.SAMPLE_SPREADSHEET_ID)
worksheet_sign_up = sh.worksheet("SignUpWorkshops")

reasons = ["Накладка в расписании", "Не успеваю", "Перезапишусь на другое время"]


@router.callback_query(StateFilter(None), F.data == "QuitWorkshop")
async def start_quiting_workshop(callback: CallbackQuery, state: FSMContext):

    sql = "SELECT * FROM workshops WHERE user_id=%s"
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            workshop = cursor.execute(sql, [callback.from_user.id]).fetchall()

    if workshop:
        await callback.message.edit_text(
            text=f"Подтвердите отмену записи на мастерскую:\n<b>{workshop[0][1]}</b>", reply_markup=get_user_accept_kb()
        )
        await state.set_state(QuitWorkshop.accepting_quit)

    else:
        await callback.message.edit_text(
            text=f"Ты не записан(а) <i>ни на одну</i> мастерскую 😥", reply_markup=get_back_to_user_menu_kb()
        )


@router.callback_query(QuitWorkshop.accepting_quit)
async def quit_accepted(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text(text="Укажите, пожалуйста причину отмены", reply_markup=get_user_list_kb(reasons))
    await state.set_state(QuitWorkshop.choosing_reason)


@router.callback_query(QuitWorkshop.choosing_reason)
async def reason_chosen(callback: CallbackQuery, state: FSMContext):

    sql = "DELETE FROM workshops WHERE user_id=%s"
    sql_workshop = "SELECT * FROM workshops WHERE user_id=%s"
    sql_quit_reason = """INSERT INTO quited_workshops (workshop, reason) VALUES (%s, %s)"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            workshop = cursor.execute(sql_workshop, [callback.from_user.id]).fetchall()
            cursor.execute(sql, [callback.from_user.id])
            cursor.execute(sql_quit_reason, [workshop[0][1], callback.data])
            conn.commit()

            if callback.from_user.id == 5444762353:
                user_name = cursor.execute(
                    "SELECT surname, name FROM users WHERE user_id=%s", [544476235]
                ).fetchall()
            else:
                user_name = cursor.execute(
                    "SELECT surname, name FROM users WHERE user_id=%s", [callback.from_user.id]
                ).fetchall()

    res = [
        i + 1
        for i, r in enumerate(worksheet_sign_up.get_all_values())
        if r[0] == workshop[0][0] and r[1] == user_name[0][0] and r[2] == user_name[0][1]
    ]
    if res:
        worksheet_sign_up.delete_rows(res[0])

    await callback.message.edit_text(
        text="Вы успешно отписались от мастерской!", reply_markup=get_back_to_user_menu_kb()
    )
    await state.clear()
