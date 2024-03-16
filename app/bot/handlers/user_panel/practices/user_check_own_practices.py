import psycopg
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.utils.markdown import hlink
from django.conf import settings

from bot.services.messages import get_lessons_with_user_id
from bot.services.keyboards import (
    get_back_to_user_menu_kb,
    get_back_to_user_practice_menu_kb,
    get_back_to_user_own_practices_menu_kb,
)

DATABASE_URL = settings.DATABASE_URL


class UserCheckOwnPractices(StatesGroup):
    choosing_practice = State()


router = Router()


@router.callback_query(StateFilter(None), F.data == "CheckForMyPractices")
async def checking_for_practices(callback: CallbackQuery, state: FSMContext):
    lessons = get_lessons_with_user_id(callback.from_user.id)

    if len(lessons) == 0:
        await callback.message.edit_text(
            text="😥 Вы не записаны ни на одно занятие", reply_markup=get_back_to_user_menu_kb()
        )
    else:

        await callback.message.edit_text(
            text="Для подробной информации выбери нужное занятие",
            reply_markup=get_back_to_user_practice_menu_kb(lessons),
        )
        await state.set_state(UserCheckOwnPractices.choosing_practice)


@router.callback_query(UserCheckOwnPractices.choosing_practice)
async def practice_chosen(callback: CallbackQuery, state: FSMContext):
    sql_practice_info = "SELECT * FROM practices WHERE user_id=%s AND lessons=%s"
    sql_add_info = """SELECT * FROM schedule WHERE
                    lesson=%s AND format=%s AND date=%s AND hours=%s AND minutes=%s"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            practice = cursor.execute(sql_practice_info, [callback.from_user.id, callback.data]).fetchall()
            add_info = cursor.execute(
                sql_add_info, [practice[0][1], practice[0][2], practice[0][3], practice[0][4], practice[0][5]]
            ).fetchall()
            conn.commit()

    if add_info[0][6][0] in "0123456789":
        await callback.message.edit_text(
            text=f"Ты записан(а) на занятие <b>{practice[0][1]}</b>\n\n🎯 Формат: <b>{practice[0][2]}</b>"
            + f"\n📍 Аудитория: <b>{add_info[0][6]}</b>\n\n📆 Дата: <b>{practice[0][3]}</b>\n🕑 Время: <b>{practice[0][4]}:{practice[0][5]}</b>",
            reply_markup=get_back_to_user_own_practices_menu_kb(),
        )
    else:
        link = hlink("ссылка", add_info[0][6])
        await callback.message.edit_text(
            text=f"Ты записан(а) на занятие <b>{practice[0][1]}</b>\n\n🎯 Формат: <b>{practice[0][2]}</b>"
            + f"\n💻 Ссылка на Zoom: {link}\n\n📆 Дата: <b>{practice[0][3]}</b>\n🕑 Время: <b>{practice[0][4]}:{practice[0][5]}</b>",
            reply_markup=get_back_to_user_own_practices_menu_kb(),
            disable_web_page_preview=True,
        )
    await state.clear()
