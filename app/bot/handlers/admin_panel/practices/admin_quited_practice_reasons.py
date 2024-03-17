import psycopg
from aiogram import Router, F
from aiogram.types import CallbackQuery
from django.conf import settings

from bot.services.keyboards import get_back_to_admin_menu_kb

DATABASE_URL = settings.DATABASE_URL


router = Router()


@router.callback_query(F.data == "CheckQuitReasons")
async def start_checking_reasons(callback: CallbackQuery):

    sql = """SELECT * FROM quited_practice"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            tuple_reasons = cursor.execute(sql).fetchall()

    reasons = []
    for x in tuple_reasons:
        reasons.append(x[0] + ": " + x[1])
    reasons = "\n".join(reasons)
    if reasons:
        await callback.message.edit_text(text=f"{reasons}", reply_markup=get_back_to_admin_menu_kb())
    else:
        await callback.message.edit_text(text="Отказов пока не было", reply_markup=get_back_to_admin_menu_kb())