from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from bot.services.keyboards import get_user_sign_or_quit_practice_kb

router = Router()


@router.callback_query(F.data == "SignOrQuitPractice")
async def sign_or_quit(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        text="<b>Занятия</b>\n\nЗдесь можно <i>записаться</i> на занятие или <i>отменить</i> запись.\n\n"
        + "⚡️ <u>Занятия, которые состоятся на неделе <b>18.03 - 22.03</b></u>:\n\n"
        + "<b>Техническое оснащение аудиторий ИТМО</b> (2 ак.ч.)\nпреподаватель: Новожилов А. С.\n"
        + "1. 22.03, 17:00-18:30 - Кронверкский пр., д. 49, ауд. 1316.\n\n"
        + "<b>Рефлексивная конференция</b> (2 ак.ч.)\nПреподаватель: Безызвестных Е. А.\n"
        + "1. 22.03, 10:00-11:30 - Zoom.\n\n"
        + "⚡️ <u>Занятия, которые состоятся на неделе <b>25.03 - 29.03</b></u>:\n\n"
        + "<b>Техническое оснащение аудиторий ИТМО</b> (2 ак.ч.)\nпреподаватель: Новожилов А. С.\n"
        + "1. 27.03, 11:40-13:10 - ул. Ломоносова, д. 9, ауд. 1310.\n\n"
        + "<b>Рефлексивная конференция</b> (2 ак.ч.)\nПреподаватель: Безызвестных Е. А.\n"
        + "1. 25.03, 17:00-18:30 - Zoom.\n\n"
        + "<b>Правила педагогической коммуникации</b> (2 ак.ч.)\nПреподаватель: Безызвестных Е. А.\n"
        + "1. 26.03, 10:00-11:30 - Zoom.\n\n"
        + "⚡️ <u>Занятия, которые состоятся на неделе <b>01.04 - 05.04</b></u>:\n\n"
        + "<b>Правила педагогической коммуникации</b> (2 ак.ч.)\nПреподаватель: Безызвестных Е. А.\n"
        + "1. 01.04, 17:00-18:30 - Zoom.\n\n",

        reply_markup=get_user_sign_or_quit_practice_kb(),
    )

    await state.clear()
