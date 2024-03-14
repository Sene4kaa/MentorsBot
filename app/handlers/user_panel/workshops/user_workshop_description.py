from aiogram import Router, F
from aiogram.types import CallbackQuery


router = Router()


@router.callback_query(F.data == "WorkshopDescriptions")
async def checking_descriptions(callback: CallbackQuery):
    await callback.answer(text="❗️ Раздел в разработке", show_alert=True)
