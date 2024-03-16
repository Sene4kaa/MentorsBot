from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink

from bot.services.keyboards import get_back_to_user_menu_kb


router = Router()


@router.callback_query(F.data == "Connect")
async def send_message(callback: CallbackQuery):
    
    chat_link = hlink("Чат", "https://t.me/+YxoRDu70TpVmYzVi")
    await callback.message.edit_text(
        text=f"Контакты:\n\n{chat_link} - ссылка на чат\neabezyzvestnykh@itmo.ru - почта\n\nПо вопросам работы бота:\nadosychenko@itmo.ru", 
        reply_markup=get_back_to_user_menu_kb()
    )
