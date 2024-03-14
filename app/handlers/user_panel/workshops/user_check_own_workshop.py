import psycopg
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.utils.markdown import hlink

from config import DATABASE_URL
from services.messages import get_workshops_with_user_id
from services.keyboards import (
    get_back_to_user_menu_kb,
    get_back_to_user_own_workshop_menu_kb,
    get_back_to_user_workshop_menu_kb,
)


class UserCheckOwnWorkshops(StatesGroup):
    choosing_workshop = State()


router = Router()


@router.callback_query(StateFilter(None), F.data == "CheckOwnWorkshop")
async def checking_for_workshops(callback: CallbackQuery, state: FSMContext):

    lessons = get_workshops_with_user_id(callback.from_user.id)

    if len(lessons) == 0:
        await callback.message.edit_text(
            text="😥 Вы не записаны ни на одну мастерскую", reply_markup=get_back_to_user_menu_kb()
        )
    else:

        await callback.message.edit_text(
            text="Для получения <u>номера аудитории</u> или <u>ссылки для подключения</u> выбери нужную мастерскую",
            reply_markup=get_back_to_user_workshop_menu_kb(lessons),
        )
        await state.set_state(UserCheckOwnWorkshops.choosing_workshop)


@router.callback_query(UserCheckOwnWorkshops.choosing_workshop)
async def workshop_chosen(callback: CallbackQuery, state: FSMContext):

    sql_workshop_info = "SELECT * FROM workshops WHERE user_id=%s AND title=%s"
    sql_add_info = """SELECT * FROM workshops_schedule WHERE
                    title=%s AND format=%s AND date=%s AND hours=%s AND minutes=%s"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            workshop = cursor.execute(sql_workshop_info, [callback.from_user.id, callback.data]).fetchall()
            add_info = cursor.execute(
                sql_add_info, [workshop[0][1], workshop[0][2], workshop[0][3], workshop[0][4], workshop[0][5]]
            ).fetchall()
            conn.commit()

    if add_info[0][6][0] in "0123456789":
        await callback.message.edit_text(
            text=f"Ты записан(а) на мастерскую\n🧠 Название: <b>{workshop[0][1]}</b>\n\n🎯 Формат: <b>{workshop[0][2]}</b>"
            + f"\n📍 Аудитория: <b>{add_info[0][6]}</b>\n\n📆 Дата: <b>{workshop[0][3]}</b>\n🕑 Время: <b>{workshop[0][4]}:{workshop[0][5]}</b>",
            reply_markup=get_back_to_user_own_workshop_menu_kb(),
        )
    else:
        link = hlink("ссылка", add_info[0][6])
        await callback.message.edit_text(
            text=f"Ты записан(а) на мастерскую\n🧠 Название: <b>{workshop[0][1]}</b>\n\n🎯 Формат: <b>{workshop[0][2]}</b>"
            + f"\n💻 Ссылка на Zoom: {link}\n\n📆 Дата: <b>{workshop[0][3]}</b>\n🕑 Время: <b>{workshop[0][4]}:{workshop[0][5]}</b>",
            reply_markup=get_back_to_user_own_workshop_menu_kb(),
            disable_web_page_preview=True,
        )
    await state.clear()
