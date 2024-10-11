from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink

from bot.services.keyboards import get_back_to_user_menu_kb


router = Router()


@router.callback_query(F.data == "Connect")
async def send_message(callback: CallbackQuery):
    
    chat_link = hlink("Чат курса", "https://t.me/+bu3yOKgpEFpiYjI6")
    await callback.message.edit_text(
        text=f"Контакты:\n\n{chat_link} - ссылка на чат\nmentors@itmo.ru - почта\n\nПо вопросам работы бота:\nvdroy@itmo.ru",
        reply_markup=get_back_to_user_menu_kb(),
        disable_web_page_preview=True
    )
