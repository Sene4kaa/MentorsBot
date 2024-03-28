from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from bot.services.keyboards import get_user_sign_or_quit_practice_kb

router = Router()


@router.callback_query(F.data == "SignOrQuitPractice")
async def sign_or_quit(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        text="<b>Занятия</b>\nЗдесь можно <i>записаться</i> на занятие или <i>отменить</i> запись.\n\n"
        + "⚡️ <u>Занятия, которые состоятся на неделе <b>01.04 - 06.04</b></u>:\n\n"
        + "<b>Управление эмоциями в учебной среде</b> (2 ак.ч.)\n"
        + "1. 02.04, 11:40-13:10 - Zoom.\nпреподаватель: Скакун С.А.\n"
        + "2. 04.04, 13:30-15:00  - Zoom.\nпреподаватель: Романенко Ю.Н.\n\n"
        + "<b>Практикум педагогического наблюдения</b> (3 ак.ч.)\nпреподаватель: Безызвестных Е. А.\n"
        + "1. 03.04, 10:00-12:00 - Ломоносова 9, аудитория  3412.\n"
        + "2. 04.04, 15:20-17:20  - Ломоносова 9, аудитория 3407.\n\n"
        + "<b>Правила педагогической коммуникации</b> (2 ак.ч.)\nПреподаватель: Безызвестных Е. А.\n"
        + "1. 01.04, 17:00-18:30 - Zoom.",

        reply_markup=get_user_sign_or_quit_practice_kb(),
    )

    await state.clear()
