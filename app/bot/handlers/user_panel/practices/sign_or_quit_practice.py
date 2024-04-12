from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from bot.services.keyboards import get_user_sign_or_quit_practice_kb

router = Router()


@router.callback_query(F.data == "SignOrQuitPractice")
async def sign_or_quit(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        text="<b>Занятия</b>\nЗдесь можно <i>записаться</i> на занятие или <i>отменить</i> запись.\n\n"
        + "⚡️ <u>Занятия, которые состоятся на неделе <b>08.04 - 13.04</b></u>:\n\n"
        + "<b>Педагогический дизайн</b> (2 ак.ч.)\nпреподаватель: Безызвестных Е.А.\n"
        + "1. 13.04, 10:00-11:30 - Zoom.\n\n"
        + "⚡️ <u>Занятия, которые состоятся на неделе <b>15.04 - 20.04</b></u>:\n\n"
        + "<b>Менеджмент учебного процесса</b> (2 ак.ч.)\nпреподаватель: Никуленко А. А.\n"
        + "1. 15.04, 17:00-18:30 - Ломоносова 9, аудитория 3412.\n\n"
        + "<b>Педагогический дизайн</b> (2 ак.ч.)\nпреподаватель: Безызвестных Е.А.\n"
        + "1. 19.04, 17:00-18:30 - Zoom.\n\n"
        + "<b>Методика проведения лабораторных работ</b> (2 ак.ч.)\nпреподаватель: Бабкина А.\n"
        + "1. 19.04, 13:30-15:00 - Zoom.\n\n"
        + "<b>Мастер-класс \"Запуск своего факультатива: от идеи до реализации\"</b> (2 ак.ч.)\n"
        + "преподаватель: Безызвестных Е.А.\n"
        + "1. 16.04, 13:30-15:00 - Zoom.\n\n",

        reply_markup=get_user_sign_or_quit_practice_kb(),
    )

    await state.clear()
