from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from bot.services.keyboards import get_user_sign_or_quit_practice_kb

router = Router()


@router.callback_query(F.data == "SignOrQuitPractice")
async def sign_or_quit(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        text="<b>Занятия</b>\nЗдесь можно <i>записаться</i> на занятие или <i>отменить</i> запись.\n\n"

        + "⚡️ <u>Занятия, которые состоятся на неделе <b>29.04 - 04.05</b></u>:\n\n"

        + "<b>Тайм-менеджмент</b> (2 ак.ч.)\n"
        + "преподаватель: Кузьминкова А.С.\n"
        + "1. 29.04, 17:00-18:30 - Zoom.\n\n"

        + "<b>Активное обучение</b> (2 ак.ч.)\n"
        + "преподаватель: Кузнецова А.П.\n"
        + "1. 2.05, 15:20-16:50 - Zoom.\n\n"

        + "<b>Управление дискуссией</b> (4 ак.ч.)\n"
        + "преподаватель: Брусницына М.А.\n"
        + "1. 04.05, 11:40-15:00 - Кронверкский 49, аудитория 2201.\n\n",

        reply_markup=get_user_sign_or_quit_practice_kb(),
    )

    await state.clear()
