import gspread

import psycopg

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from django.conf import settings
from aiogram.utils.markdown import hlink

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

    if user_data['chosen_workshop_practice'] == "Оценивание":
        link = hlink(
            "табличке",
             "https://docs.google.com/spreadsheets/d/1hkPSwhyr5K64YQ4e8KLZd2NoKr5F6lC4Gx8SB62wU_c/edit#gid=0"
        )
        await callback.message.edit_text(
            text=f"Ты выбрал(а) мастерскую: <b>{user_data['chosen_workshop_practice']}</b>\n\n"
            + f"❗️ <b>Для занятий 2 и 4 кроме записи через бота необходима запись в {link} </b> ❗️\n\n"
            + "<u>Расписание для данной мастерской</u>:\n\n"
            + "Занятие 2. 18 апреля, 16:00-19:00, онлайн\n"
            + "Занятие 2. 19 апреля, 10:00-11:30, онлайн\n"
            + "Занятие 3. 23 апреля, 17:00-18:30, онлайн\n"
            + "Занятие 4. 7 мая, 16:00-19:00, онлайн\n"
            + "Занятие 4. 8 мая, 10:00-11:30, онлайн\n\n"
            + "<u>Индивидуальные консультации по запросу: с 15 мая по 15 июня</u>",

            reply_markup=get_user_list_cancel_sign_up_workshop_practice_kb(
                set(get_workshops_dates_lower_35_list(user_data["chosen_workshop_practice"]))
            ),
        )
    elif user_data['chosen_workshop_practice'] == "Практики пед.общения и мотивация":
        await callback.message.edit_text(
            text=f"Ты выбрал(а) мастерскую:\n<b>{user_data['chosen_workshop_practice']}</b>\n\n"
                 + "<u>Расписание для данной мастерской</u>:\n\n"
                 + "1. Очный тренинг, 24.04, 10:00-11:30 - Ломоносова 9, ауд. 1310\n"
                 + "2. Очный тренинг, 26.04, 15:20-16:50 - Ломоносова 9, ауд. 1310\n\n"
                 + "Выбери дату для участия в очном тренинге.",

            reply_markup=get_user_list_cancel_sign_up_workshop_practice_kb(
                set(get_workshops_dates_lower_35_list(user_data["chosen_workshop_practice"]))
            ),
        )
    elif user_data['chosen_workshop_practice'] == "Дизайн учебных презентаций":
        await callback.message.edit_text(
            text=f"Ты выбрал(а) мастерскую:\n<b>{user_data['chosen_workshop_practice']}</b>\n\n"
                 + "<u>Расписание для данной мастерской</u>:\n\n"
                 + "Занятие 2. 19 апреля 15:20 - 16:50, онлайн\n\n",

            reply_markup=get_user_list_cancel_sign_up_workshop_practice_kb(
                set(get_workshops_dates_lower_35_list(user_data["chosen_workshop_practice"]))
            ),
        )
    elif user_data['chosen_workshop_practice'] == "Адаптация уч.материалов":
        await callback.message.edit_text(
            text=f"Ты выбрал(а) мастерскую:\n<b>{user_data['chosen_workshop_practice']}</b>\n\n"
                 + "<u>Расписание для данной мастерской</u>:\n\n"
                 + "Занятие 3. 19 апреля 11.40-13.10, онлайн\n"
                 + "Занятие 4. 22 апреля 15.20 - 16.50, онлайн\n\n",

            reply_markup=get_user_list_cancel_sign_up_workshop_practice_kb(
                set(get_workshops_dates_lower_35_list(user_data["chosen_workshop_practice"]))
            ),
        )
    elif user_data['chosen_workshop_practice'] == "Разработка занятия":
        await callback.message.edit_text(
            text=f"Ты выбрал(а) мастерскую:\n<b>{user_data['chosen_workshop_practice']}</b>\n\n"
                 + "<u>Расписание для данной мастерской</u>:\n\n"
                 + "Занятие 1. 15 апреля 17:00-18:30, очно\n"
                 + "Занятие 2. 22 апреля 17:00-18:30, очно\n"
                 + "Занятие 3. 29 апреля 17:00-18:30, очно\n\n"
                 + "<u>Консультация с разбором плана занятия: с 7 апреля по 15 апреля</u>",

            reply_markup=get_user_list_cancel_sign_up_workshop_practice_kb(
                set(get_workshops_dates_lower_35_list(user_data["chosen_workshop_practice"]))
            ),
        )
    await state.set_state(WorkshopSignUp.choosing_time)


@router.callback_query(WorkshopSignUp.choosing_workshop_practice)
async def workshop_practice_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_workshop_practice=callback.data)
    user_data = await state.get_data()

    if user_data['chosen_workshop_practice'] == "Оценивание":
        link = hlink(
            "табличке",
            "https://docs.google.com/spreadsheets/d/1hkPSwhyr5K64YQ4e8KLZd2NoKr5F6lC4Gx8SB62wU_c/edit#gid=0"
        )
        await callback.message.edit_text(
            text=f"Ты выбрал(а) мастерскую: <b>{user_data['chosen_workshop_practice']}</b>\n\n"
                 + f"❗️<b>Для занятий 2 и 4 кроме записи через бота необходима запись в {link} </b>❗️\n\n"
                 + "<u>Расписание для данной мастерской</u>:\n\n"
                 + "Занятие 2. 18 апреля, 16:00-19:00, онлайн\n"
                 + "Занятие 2. 19 апреля, 10:00-11:30, онлайн\n"
                 + "Занятие 3. 23 апреля, 17:00-18:30, онлайн\n"
                 + "Занятие 4. 7 мая, 16:00-19:00, онлайн\n"
                 + "Занятие 4. 8 мая, 10:00-11:30, онлайн\n\n"
                 + "<u>Индивидуальные консультации по запросу: с 15 мая по 15 июня</u>",

            disable_web_page_preview=True,
            reply_markup=get_user_list_cancel_sign_up_workshop_practice_kb(
                set(get_workshops_dates_lower_35_list(user_data["chosen_workshop_practice"]))
            ),
        )
    elif user_data['chosen_workshop_practice'] == "Практики пед.общения и мотивация":
        await callback.message.edit_text(
            text=f"Ты выбрал(а) мастерскую:\n<b>{user_data['chosen_workshop_practice']}</b>\n\n"
                 + "<u>Расписание для данной мастерской</u>:\n\n"
                 + "Занятие 2. 16 апреля 15:20-16:50, онлайн\n"
                 + "Очный тренинг.  C 22 апреля по 27 апреля, дата по согласованию с участниками",

            reply_markup=get_user_list_cancel_sign_up_workshop_practice_kb(
                set(get_workshops_dates_lower_35_list(user_data["chosen_workshop_practice"]))
            ),
        )
    elif user_data['chosen_workshop_practice'] == "Дизайн учебных презентаций":
        await callback.message.edit_text(
            text=f"Ты выбрал(а) мастерскую:\n<b>{user_data['chosen_workshop_practice']}</b>\n\n"
                 + "<u>Расписание для данной мастерской</u>:\n\n"
                 + "Занятие 2. 19 апреля 15:20 - 16:50, онлайн",

            reply_markup=get_user_list_cancel_sign_up_workshop_practice_kb(
                set(get_workshops_dates_lower_35_list(user_data["chosen_workshop_practice"]))
            ),
        )
    elif user_data['chosen_workshop_practice'] == "Адаптация уч.материалов":
        await callback.message.edit_text(
            text=f"Ты выбрал(а) мастерскую:\n<b>{user_data['chosen_workshop_practice']}</b>\n\n"
                 + "<u>Расписание для данной мастерской</u>:\n\n"
                 + "Занятие 3. 19 апреля 11.40-13.10, онлайн\n"
                 + "Занятие 4. 22 апреля 15.20 - 16.50, онлайн\n\n",

            reply_markup=get_user_list_cancel_sign_up_workshop_practice_kb(
                set(get_workshops_dates_lower_35_list(user_data["chosen_workshop_practice"]))
            ),
        )
    elif user_data['chosen_workshop_practice'] == "Разработка занятия":
        await callback.message.edit_text(
            text=f"Ты выбрал(а) мастерскую:\n<b>{user_data['chosen_workshop_practice']}</b>\n\n"
                 + "<u>Расписание для данной мастерской</u>:\n\n"
                 + "Занятие 1. 15 апреля 17:00-18:30, очно\n"
                 + "Занятие 2. 22 апреля 17:00-18:30, очно\n"
                 + "Занятие 3. 29 апреля 17:00-18:30, очно\n\n"
                 + "<u>Консультация с разбором плана занятия: с 7 апреля по 15 апреля</u>",

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
                    + f"🧠 Предмет: <b>{user_data['chosen_workshop_practice']}</b>\n"
                    + f"📆 Дата и время: <b>{user_data['chosen_time']}</b>.\n\n"
                    + f"❗️ Обрати внимание ❗️\nФормат занятия: <b>{workshop_format}</b>\n"
                    + f"<u>Для того, чтобы онлайн-занятие было засчитано, необходимо включение микрофона и веб-камеры</u>"
                    + "\n<i>На каждое новое занятие нужно записываться отдельно!</i>"
                    + "\n\n<u>Подтверди запись</u>.\nP.S. Может занять некоторое время."
            ),
            reply_markup=get_user_added_workshop_practice_kb(),
        )
    else:
        await callback.message.edit_text(
            text=(
                    f"Ты хочешь записаться на мастерскую\n\n"
                    + f"🧠 Предмет: <b>{user_data['chosen_workshop_practice']}</b>\n"
                    + f"📆 Дата и время: <b>{user_data['chosen_time']}</b>.\n\n"
                    + f"❗️ Обрати внимание ❗️\nФормат занятия: <b>{workshop_format}</b>"
                    + "\n<i>На каждое новое занятие нужно записываться отдельно!</i>"
                    + "\n\n<u>Подтверди запись</u>.\nМожет занять некоторое время."
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

            user_name = cursor.execute(
                "SELECT surname, name FROM users WHERE user_id=%s", [callback.from_user.id]
            ).fetchall()

            conn.commit()
    # Добавление участника в гугл-таблицу

    gc = gspread.service_account(filename="test.json")
    sh = gc.open_by_key(settings.SAMPLE_SPREADSHEET_ID)
    worksheet_sign_up = sh.worksheet("SignUpWorkshops")
    next_row_id = str(int(next_available_row(worksheet_sign_up)) + 1)

    if (worksheet_sign_up.cell(int(next_row_id) - 1, 1).value != user_data["chosen_workshop_practice"]
        or worksheet_sign_up.cell(int(next_row_id) - 1, 2).value != user_name[0][0]
        or worksheet_sign_up.cell(int(next_row_id) - 1, 3).value != user_name[0][1]
        or worksheet_sign_up.cell(int(next_row_id) - 1, 4).value != user_data["chosen_time"].split(", ")[0] + ", " +
            user_data["chosen_time"].split(", ")[1]
        or worksheet_sign_up.cell(int(next_row_id) - 1, 5).value != user_data["chosen_time"].split(", ")[2]
        or worksheet_sign_up.cell(int(next_row_id) - 1, 6).value != "Записан(а)"):

        worksheet_sign_up.update_acell(f"A{next_row_id}", user_data["chosen_workshop_practice"])
        worksheet_sign_up.update_acell(f"B{next_row_id}", user_name[0][0])
        worksheet_sign_up.update_acell(f"C{next_row_id}", user_name[0][1])
        worksheet_sign_up.update_acell(
            f"D{next_row_id}", user_data["chosen_time"].split(", ")[0] + ", " + user_data["chosen_time"].split(", ")[1])
        worksheet_sign_up.update_acell(f"E{next_row_id}", user_data["chosen_time"].split(", ")[2])
        worksheet_sign_up.update_acell(f"F{next_row_id}", "Записан(а)")

    await callback.message.edit_text(
        text=(
            "Запись на мастерскую <b>подтверждена</b>!\n"
            "Ссылку для подключения или номер аудитории можно найти в разделе <i>Мои занятия</i>"
        ),
        reply_markup=get_back_to_user_menu_kb(),
    )
    await state.clear()
