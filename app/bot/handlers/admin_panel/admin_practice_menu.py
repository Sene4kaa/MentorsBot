from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.services.keyboards import get_admin_practice_menu_kb


router = Router()


@router.callback_query(F.data == "AdminPractice")
async def admin_practice_menu(callback: CallbackQuery):

    await callback.message.edit_text(text="Меню", reply_markup=get_admin_practice_menu_kb())
