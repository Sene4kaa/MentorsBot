from aiogram import F, Router
from aiogram.types import CallbackQuery

from services.keyboards import get_admin_workshop_menu_kb


router = Router()


@router.callback_query(F.data == "AdminWorkshop")
async def admin_workshop_menu(callback: CallbackQuery):

    await callback.message.edit_text(text="Меню", reply_markup=get_admin_workshop_menu_kb())
