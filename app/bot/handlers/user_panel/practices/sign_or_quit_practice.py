from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from bot.services.keyboards import get_user_sign_or_quit_practice_kb

router = Router()


@router.callback_query(F.data == "SignOrQuitPractice")
async def sign_or_quit(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        text="<b>Занятия</b>\n\nЗдесь можно <i>записаться</i> на занятие или <i>отменить</i> запись.\n\n"
        + "Занятия, которые состоятся на неделе <b>18.03 - 22.03</b>:\n\n"
        + "<b>Техническое оснащение аудиторий ИТМО</b> (2 ак.ч.)\nпреподаватель: Новожилов А. С.\n"
        + "1. 20.03, 11:40-13:10 - ул. Ломоносова, д. 9, ауд. 1223.\n"
        + "2. 22.03, 17:00-18:30 - Кронверкский пр., д. 49, ауд. 1316.\n\n"
        + "<b>Рефлексивная конференция</b> (2 ак.ч.)\nПреподаватель: Безызвестных Е. А.\n"
        + "1. 19.03, 10:00-11:30 - Zoom.\n"
        + "2. 23.03, 10:00-11:30 - Zoom.",
        reply_markup=get_user_sign_or_quit_practice_kb(),
    )

    await state.clear()
