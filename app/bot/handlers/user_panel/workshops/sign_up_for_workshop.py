import gspread

import psycopg

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from django.conf import settings

from bot.services.messages import (
    get_workshops_lower_35_list,
    get_workshops_format_list,
    get_deleting_workshops_list,
    get_workshops_dates_lower_35_list
)
from bot.services.keyboards import (
    get_back_to_user_menu_kb,
    get_user_list_cancel_workshop_sign_up,
    get_user_list_cancel_sign_up_workshop_practice_kb,
    get_user_added_workshop_practice_kb,
)

DATABASE_URL = settings.DATABASE_URL


class WorkshopSignUp(StatesGroup):
    signing_up_starting = State()
    choosing_workshop_practice = State()
    choosing_time = State()
    signing_up = State()


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list) + 1)


router = Router()


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

    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Ты выбрал(а) мастерскую:\n<b>{user_data['chosen_workshop_practice']}</b>\n\n"
        + f"Выбери удобные <i>дату и время</i> мастерской",
        reply_markup=get_user_list_cancel_sign_up_workshop_practice_kb(
            set(get_workshops_dates_lower_35_list(user_data["chosen_workshop_practice"]))
        ),
    )

    await state.set_state(WorkshopSignUp.choosing_time)


@router.callback_query(WorkshopSignUp.choosing_workshop_practice)
async def workshop_practice_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_workshop_practice=callback.data)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Ты выбрал(а) мастерскую:\n<b>{user_data['chosen_workshop_practice']}</b>\n\n"
        + "Выбери удобные <i>дату и время</i> мастерской",
        reply_markup=get_user_list_cancel_sign_up_workshop_practice_kb(
            set(get_workshops_dates_lower_35_list(user_data["chosen_workshop_practice"]))
        ),
    )

    await state.set_state(WorkshopSignUp.choosing_time)


@router.callback_query(WorkshopSignUp.choosing_time)
async def time_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_time=callback.data)
    user_data = await state.get_data()

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            workshop_format = cursor.execute("""SELECT format FROM workshops_schedule WHERE title=%s AND date=%s""",
                                             [user_data["chosen_workshop_practice"],
                                              user_data["chosen_time"].split(', ')[0] + ', ' +
                                              user_data["chosen_time"].split(', ')[1]]).fetchall()[0][0]
            conn.commit()

    await state.update_data(chosen_format=workshop_format)

    if workshop_format == "Zoom":
        await callback.message.edit_text(
            text=(
                    f"Ты хочешь записаться на мастерскую\n\n"
                    + f"🧠 Предмет: <b>{user_data['chosen_workshop_practice']}</b>\n\n"
                    + f"❗️ Обрати внимание ❗️\nФормат занятия: <b>{workshop_format}</b>\n"
                    + f"<u>Для того, чтобы онлайн-занятие было засчитано, необходимо включение микрофона и веб-камеры</u>"
                    + f"\n📆 Дата и время: <b>{user_data['chosen_time']}</b>."
                    + "\n\n<u>Подтверди запись</u>."
            ),
            reply_markup=get_user_added_workshop_practice_kb(),
        )
    else:
        await callback.message.edit_text(
            text=(
                    f"Ты хочешь записаться на занятие\n\n"
                    + f"🧠 Предмет: <b>{user_data['chosen_workshop_practice']}</b>\n\n"
                    + f"❗️ Обрати внимание ❗️\nФормат занятия: <b>{workshop_format}</b>\n"
                    + f"📆 Дата и время: <b>{user_data['chosen_time']}</b>."
                    + "\n\n<u>Подтверди запись</u>."
            ),
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
            if callback.from_user.id == 5444762353:
                user_name = cursor.execute(
                    "SELECT surname, name FROM users WHERE user_id=%s", [544476235]
                ).fetchall()
            else:
                user_name = cursor.execute(
                    "SELECT surname, name FROM users WHERE user_id=%s", [callback.from_user.id]
                ).fetchall()
    # Добавление участника в гугл-таблицу

    gc = gspread.service_account(filename="test.json")
    sh = gc.open_by_key(settings.SAMPLE_SPREADSHEET_ID)
    worksheet_sign_up = sh.worksheet("SignUpWorkshops")

    next_row_id = str(int(next_available_row(worksheet_sign_up)) + 1)
    worksheet_sign_up.update_acell(f"A{next_row_id}", user_data["chosen_workshop_practice"])
    worksheet_sign_up.update_acell(f"B{next_row_id}", user_name[0][0])
    worksheet_sign_up.update_acell(f"C{next_row_id}", user_name[0][1])
    worksheet_sign_up.update_acell(
        f"D{next_row_id}", user_data["chosen_time"].split(", ")[0] + ", " + user_data["chosen_time"].split(", ")[1])
    worksheet_sign_up.update_acell(f"E{next_row_id}", user_data["chosen_time"].split(", ")[2])

    await callback.message.edit_text(
        text=(
            "Запись на мастерскую <b>подтверждена</b>!\n"
            "Ссылку для подключения или номер аудитории можно найти в разделе <i>Мои занятия</i>"
        ),
        reply_markup=get_back_to_user_menu_kb(),
    )
    await state.clear()
