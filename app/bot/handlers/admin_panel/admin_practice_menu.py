from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.services.keyboards import get_admin_practice_menu_kb


router = Router()


@router.callback_query(F.data == "AdminPractice")
async def admin_practice_menu(callback: CallbackQuery):

    await callback.message.edit_text(
        text=(
            "Меню\n\n"
            + "<b>Посмотреть участников</b> - посмотреть фамилии и имена участников конкретного занятия\n\n"
            + "<b>Добавить мастерскую</b> - добавить <u>название</u> занятия.\n\n"
            + "<b>Удалить мастерскую</b> - удалить занятие <u>полностью</u>.\n\n"
            + "<b>Добавить занятие в мастерскую</b> - добавить занятие в расписание.\n\n"
            + "<b>Удалить занятие из мастерской</b> - удалить конкретное занятие из расписания.\n\n"
            + "<b>Посмотреть отказы</b> - посмотреть причины отказов от занятий."
        ),
        reply_markup=get_admin_practice_menu_kb())
