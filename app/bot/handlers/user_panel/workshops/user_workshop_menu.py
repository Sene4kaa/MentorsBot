from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.services.keyboards import get_user_workshop_menu_kb

router = Router()


@router.callback_query(F.data == "Workshops")
async def workshop_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=(
            "<b>Мастерские</b> \n\nЗдесь можно <i>записаться</i> на мастерские или <i>отменить</i> запись.\n"
            "Посещение хотя бы одной мастерской является <u>обязательным</u> условием прохождения курса.\n\n"
        ),
        reply_markup=get_user_workshop_menu_kb(),
    )
    await state.clear()
