from aiogram import F, Router
from aiogram.types import CallbackQuery

from services.keyboards import get_back_to_user_menu_kb


router = Router()

@router.callback_query(F.data == "Connect")
async def send_message(callback: CallbackQuery):

    await callback.message.edit_text(
        text=(
            "<b>Контакты</b>:\n\nhttps://t.me/+YxoRDu70TpVmYzVi - ссылка на чатик\n - почта"
            + "\n\nПо вопросам работы бота:\nadosychenko@itmo.ru"
        ),
        reply_markup=get_back_to_user_menu_kb()
    )

