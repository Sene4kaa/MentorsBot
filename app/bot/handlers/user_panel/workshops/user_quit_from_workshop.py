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
    choosing_workshop = State()
    accepting_quit = State()
    choosing_reason = State()


router = Router()

gc = gspread.service_account(filename="test.json")
sh = gc.open_by_key(settings.SAMPLE_SPREADSHEET_ID)
worksheet_sign_up = sh.worksheet("SignUpWorkshops")

reasons = ["Накладка в расписании", "Не успеваю", "Перезапишусь на другое время"]


@router.callback_query(StateFilter(None), F.data == "QuitWorkshop")
async def start_quiting_workshop(callback: CallbackQuery, state: FSMContext):

    sql = "SELECT title FROM workshops WHERE user_id=%s"
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            workshop_titles = cursor.execute(sql, [callback.from_user.id]).fetchall()

    if workshop_titles:

        workshop = []
        for x in workshop_titles:
            workshop.append(x[0])

        await callback.message.edit_text(
            text=f"Выберите мастерскую, от которой хотите описаться 👀",
            reply_markup=get_user_list_kb(workshop)
        )
        await state.set_state(QuitWorkshop.choosing_workshop)

    else:
        await callback.message.edit_text(
            text=f"Ты не записан(а) <i>ни на одну</i> мастерскую 😥", reply_markup=get_back_to_user_menu_kb()
        )


@router.callback_query(QuitWorkshop.choosing_workshop)
async def quit_accepted(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_workshop=callback.data)

    await callback.message.edit_text(text="Укажите, пожалуйста причину отмены", reply_markup=get_user_list_kb(reasons))
    await state.set_state(QuitWorkshop.choosing_reason)


@router.callback_query(QuitWorkshop.choosing_reason)
async def reason_chosen(callback: CallbackQuery, state: FSMContext):

    user_data = await state.get_data()

    sql = "DELETE FROM workshops WHERE user_id=%s AND title=%s"
    sql_schedule_info = "SELECT * FROM workshops WHERE user_id=%s AND title=%s"

    sql_schedule = """UPDATE workshops_schedule 
            SET users_number = users_number - 1 
            WHERE title=%s AND format=%s AND date=%s AND hours=%s AND minutes=%s"""

    sql_workshop = "SELECT * FROM workshops WHERE user_id=%s"
    sql_quit_reason = """INSERT INTO quited_workshops (workshop, reason) VALUES (%s, %s)"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            workshop = cursor.execute(sql_workshop, [callback.from_user.id]).fetchall()
            cursor.execute(sql_quit_reason, [workshop[0][1], callback.data])

            schedule_info = cursor.execute(sql_schedule_info,
                                           [callback.from_user.id, user_data['chosen_workshop']]).fetchall()

            cursor.execute(sql_schedule, [schedule_info[0][1], schedule_info[0][2], schedule_info[0][3],
                                          schedule_info[0][4], schedule_info[0][5]])

            user_name = cursor.execute(
                "SELECT surname, name FROM users WHERE user_id=%s", [callback.from_user.id]
            ).fetchall()

            res = [
                i + 1
                for i, r in enumerate(worksheet_sign_up.get_all_values())
                if r[0] == user_data['chosen_workshop'] and r[1] == user_name[0][0] and r[2] == user_name[0][1]
                and r[5] != "Отписан(а)"
            ]
            for cell in res:
                worksheet_sign_up.update_acell(f"F{cell}", "Отписан(а)")

            cursor.execute(sql, [callback.from_user.id, user_data['chosen_workshop']])
            conn.commit()

    await callback.message.edit_text(
        text="Вы успешно отписались от мастерской!", reply_markup=get_back_to_user_menu_kb()
    )
    await state.clear()
