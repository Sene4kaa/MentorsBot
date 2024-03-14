import gspread

import psycopg

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from config import DATABASE_URL, SAMPLE_SPREADSHEET_ID
from services.messages import get_workshops_lower_35_list, get_workshops_format_list, get_deleting_workshops_list
from services.keyboards import (
    get_back_to_user_menu_kb,
    get_user_list_cancel_workshop_sign_up,
    get_user_list_cancel_sign_up_workshop_practice_kb,
    get_user_added_workshop_practice_kb,
)


class WorkshopSignUp(StatesGroup):
    signing_up_starting = State()
    choosing_workshop_practice = State()
    choosing_time = State()
    signing_up = State()


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list) + 1)


router = Router()

gc = gspread.service_account(filename="test.json")
sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID)
worksheet_sign_up = sh.worksheet("SignUpWorkshops")


available_workshop_practice_formats = ["Zoom", "Очно, Кронверкский", "Очно, Ломоносова"]


@router.callback_query(StateFilter(None), F.data == "SignUpForWorkshopPractice")
async def start_signing_up(callback: CallbackQuery, state: FSMContext):

    lessons_list = get_workshops_lower_35_list(callback.from_user.id)

    if len(lessons_list) > 0:
        await callback.message.edit_text(
            text="Какую <i>мастерскую</i> тебе хотелось бы посетить?",
            reply_markup=get_user_list_cancel_workshop_sign_up(set(lessons_list)),
        )

        await state.set_state(WorkshopSignUp.choosing_workshop_practice)
    else:
        await callback.message.edit_text(
            text="😪 Нет доступных для записи мастерских", reply_markup=get_back_to_user_menu_kb()
        )

        await state.clear()


@router.callback_query(F.data == "CancelToChoosingWorkshopPracticeOperation")
async def start_signing_up(callback: CallbackQuery, state: FSMContext):

    lessons_list = get_workshops_lower_35_list(callback.from_user.id)

    if len(lessons_list) > 0:
        await callback.message.edit_text(
            text="Какую <i>мастерскую</i> тебе хотелось бы посетить?",
            reply_markup=get_user_list_cancel_workshop_sign_up(set(lessons_list)),
        )

        await state.set_state(WorkshopSignUp.choosing_workshop_practice)
    else:
        await callback.message.edit_text(
            text="😪 Нет доступных для записи мастерских", reply_markup=get_back_to_user_menu_kb()
        )

        await state.clear()


@router.callback_query(F.data == "CancelToChoosingWorkshopDatetimeOperation")
async def time_chosen(callback: CallbackQuery, state: FSMContext):

    workshop_practice = get_workshops_format_list(callback.data)[0]
    await state.update_data(chosen_format=workshop_practice)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Ты выбрал(а) мастерскую: <b>{user_data['chosen_workshop_practice']}</b>\n\n"
        + f"❗️ Обрати внимание ❗️\nФормат занятия: <b>{user_data['chosen_format']}</b>\n\nВыбери удобные <i>дату и время</i> занятия",
        reply_markup=get_user_list_cancel_sign_up_workshop_practice_kb(
            get_deleting_workshops_list(user_data["chosen_workshop_practice"], user_data["chosen_format"])
        ),
    )

    await state.set_state(WorkshopSignUp.choosing_time)


@router.callback_query(WorkshopSignUp.choosing_workshop_practice)
async def workshop_practice_chosen(callback: CallbackQuery, state: FSMContext):

    workshop_practice = get_workshops_format_list(callback.data)[0]
    await state.update_data(chosen_format=workshop_practice)
    await state.update_data(chosen_workshop_practice=callback.data)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Ты выбрал(а) мастерскую: <b>{user_data['chosen_workshop_practice']}</b>\n\n"
        + f"❗️ Обрати внимание ❗️\nФормат занятия: <b>{user_data['chosen_format']}</b>\n\nВыбери удобные <i>дату и время</i> занятия",
        reply_markup=get_user_list_cancel_sign_up_workshop_practice_kb(
            set(get_deleting_workshops_list(user_data["chosen_workshop_practice"], user_data["chosen_format"]))
        ),
    )

    await state.set_state(WorkshopSignUp.choosing_time)


@router.callback_query(WorkshopSignUp.choosing_time)
async def time_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_time=callback.data)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Ты хочешь записаться на мастерскую\n\n🧠 Название: <b>{user_data['chosen_workshop_practice']}</b>\n🎯 Формат: <b>{user_data['chosen_format']}</b>"
        + f"\n📆 Дата и время: <b>{user_data['chosen_time']}</b>.\n\n<u>Подтверди запись</u>.",
        reply_markup=get_user_added_workshop_practice_kb(),
    )

    await state.set_state(WorkshopSignUp.signing_up)


@router.callback_query(WorkshopSignUp.signing_up)
async def ending_adding_workshop_practice(callback: CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    sql_workshop_practices = """INSERT INTO workshops (user_id, title, format, date, hours, minutes)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    sql_schedule = """UPDATE workshops_schedule 
            SET users_number = users_number + 1 
            WHERE title=%s AND format=%s AND date=%s AND hours=%s AND minutes=%s"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                sql_workshop_practices,
                [
                    callback.from_user.id,
                    user_data["chosen_workshop_practice"],
                    user_data["chosen_format"],
                    user_data["chosen_time"].split(", ")[0] + ", " + user_data["chosen_time"].split(", ")[1],
                    user_data["chosen_time"].split(", ")[2][:2],
                    user_data["chosen_time"].split(", ")[2][3:],
                ],
            )
            cursor.execute(
                sql_schedule,
                [
                    user_data["chosen_workshop_practice"],
                    user_data["chosen_format"],
                    user_data["chosen_time"].split(", ")[0] + ", " + user_data["chosen_time"].split(", ")[1],
                    user_data["chosen_time"].split(", ")[2][:2],
                    user_data["chosen_time"].split(", ")[2][3:],
                ],
            )
            conn.commit()

            user_name = cursor.execute(
                "SELECT surname, name FROM users WHERE user_id=%s", [callback.from_user.id]
            ).fetchall()
    # Добавление участника в гугл-таблицу
    next_row_id = str(int(next_available_row(worksheet_sign_up)) + 1)
    worksheet_sign_up.update_acell(f"A{next_row_id}", user_data["chosen_workshop_practice"])
    worksheet_sign_up.update_acell(f"B{next_row_id}", user_name[0][0])
    worksheet_sign_up.update_acell(f"C{next_row_id}", user_name[0][1])

    await callback.message.edit_text(
        text=(
            "Запись на мастерскую <b>подтверждена</b>!\n"
            "Ссылку для подключения или номер аудитории можно найти в разделе <i>Мои занятия</i>"
        ),
        reply_markup=get_back_to_user_menu_kb(),
    )
    await state.clear()
