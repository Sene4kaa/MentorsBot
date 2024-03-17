from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.services.keyboards import get_admin_workshop_menu_kb


router = Router()


@router.callback_query(F.data == "AdminWorkshop")
async def admin_workshop_menu(callback: CallbackQuery):

    await callback.message.edit_text(
        text=(
            "Меню\n\n"
            + "<b>Посмотреть участников</b> - посмотреть фамилии и имена участников конкретной мастерской\n\n"
            + "<b>Добавить мастерскую</b> - добавить <u>название</u> мастерской.\n\n"
            + "<b>Удалить мастерскую</b> - удалить мастерскую <u>полностью</u>.\n\n"
            + "<b>Добавить занятие в мастерскую</b> - добавить занятие по мастерской в расписание.\n\n"
            + "<b>Удалить занятие из мастерской</b> - удалить конкретное занятие по мастерской из расписания.\n\n"
            + "<b>Посмотреть отказы</b> - посмотреть причины отказов от мастерских."
        ),
        reply_markup=get_admin_workshop_menu_kb())
