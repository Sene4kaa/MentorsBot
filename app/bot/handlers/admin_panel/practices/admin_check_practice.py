import psycopg
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.utils.markdown import hlink
from django.conf import settings

from bot.services.messages import (
    get_lessons_with_user_id,
    get_lessons_dates_lower_35_list
)
from bot.services.keyboards import (
    get_admin_list_kb,
    get_back_to_admin_menu_kb,
    get_admin_list_cancel_sign_up_practice_kb,
    get_admin_added_practice_kb
)

DATABASE_URL = settings.DATABASE_URL


class AdminCheckPractices(StatesGroup):
    choosing_practice = State()
    choosing_time = State()
    go_to_menu = State()


router = Router()


@router.callback_query(StateFilter(None), F.data == "AdminCheckPractices")
async def checking_for_practices(callback: CallbackQuery, state: FSMContext):

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            tuple_practices = cursor.execute("""SELECT DISTINCT lesson FROM schedule""").fetchall()
            conn.commit()

    practices = []
    for practice in tuple_practices:
        practices.append(practice[0])

    await callback.message.edit_text(
        text="Для подробной информации выбери нужное занятие",
        reply_markup=get_admin_list_kb(practices),
    )
    await state.set_state(AdminCheckPractices.choosing_practice)


@router.callback_query(F.data == "AdminCancelToChoosingPracticeOperation")
async def back_to_choosing_practices(callback: CallbackQuery, state: FSMContext):

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            tuple_practices = cursor.execute("""SELECT DISTINCT lesson FROM schedule""").fetchall()
            conn.commit()

    practices = []
    for practice in tuple_practices:
        practices.append(practice[0])

    await callback.message.edit_text(
        text="Для подробной информации выбери нужное занятие",
        reply_markup=get_admin_list_kb(practices),
    )
    await state.set_state(AdminCheckPractices.choosing_practice)


@router.callback_query(AdminCheckPractices.choosing_practice)
async def practice_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_practice=callback.data)
    admin_data = await state.get_data()

    await callback.message.edit_text(
        text=(
            f"Ты выбрал(а) занятие: <b>{admin_data['chosen_practice']}</b>"
            + "\n\nВыбери <i>дату и время</i> занятия"
        ),
        reply_markup=get_admin_list_cancel_sign_up_practice_kb(
            set(get_lessons_dates_lower_35_list(admin_data["chosen_practice"]))
        ),
    )
    await state.set_state(AdminCheckPractices.choosing_time)


@router.callback_query(F.data == "AdminCancelToChoosingDatetimeOperation")
async def back_to_choosing_time(callback: CallbackQuery, state: FSMContext):

    admin_data = await state.get_data()
    print(admin_data)

    await callback.message.edit_text(
        text=(
                f"Ты выбрал(а) занятие: <b>{admin_data['chosen_practice']}</b>"
                + "\n\nВыбери <i>дату и время</i> занятия"
        ),
        reply_markup=get_admin_list_cancel_sign_up_practice_kb(
            set(get_lessons_dates_lower_35_list(admin_data["chosen_practice"]))
        ),
    )
    await state.set_state(AdminCheckPractices.choosing_time)


@router.callback_query(AdminCheckPractices.choosing_time)
async def time_chosen(callback: CallbackQuery, state: FSMContext):

    sql_practice_info = "SELECT * FROM schedule WHERE lesson=%s AND date=%s"

    admin_data = await state.get_data()
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            practice = cursor.execute(sql_practice_info,
                                      [admin_data['chosen_practice'],
                                       callback.data.split(', ')[0] + ', ' + callback.data.split(', ')[1]]
                                      ).fetchall()[0]
            conn.commit()

    if practice[6][0] in "0123456789":
        await callback.message.edit_text(
            text=f"Ты записан(а) на занятие <b>{practice[0]}</b>\n\n🎯 Формат: <b>{practice[1]}</b>"
            + f"\n📍 Аудитория: <b>{practice[6]}</b>\n\n📆 Дата: <b>{practice[2]}</b>\n🕑 Время: <b>{practice[3]}:{practice[4]}</b>",
            reply_markup=get_back_to_admin_menu_kb(),
        )
    else:
        link = hlink("ссылка", practice[6])
        await callback.message.edit_text(
            text=f"Ты записан(а) на занятие <b>{practice[0]}</b>\n\n🎯 Формат: <b>{practice[1]}</b>"
            + f"\n💻 Ссылка на Zoom: {link}\n\n📆 Дата: <b>{practice[2]}</b>\n🕑 Время: <b>{practice[3]}:{practice[4]}</b>",
            reply_markup=get_admin_added_practice_kb(),
            disable_web_page_preview=True,
        )
