from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from bot.services.keyboards import get_user_sign_or_quit_practice_kb

router = Router()


@router.callback_query(F.data == "SignOrQuitPractice")
async def sign_or_quit(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        text="<b>Занятия</b>\nЗдесь можно <i>записаться</i> на занятие или <i>отменить</i> запись.\n\n"\
        + "⚡️ <u>Занятия, которые состоятся на неделе <b>14.10 - 18.10</b></u>:\n\n" \
        + "<b>Менеджмент учебного процесса (2 ак.ч)</b>\n"\
        + "Преподаватель: Никуленко А.А.\n"\
        + "1. 14 октября 17:00-18:30 – ул. Ломоносова, д.9., ауд. 3109\n"\
        + "2. 15 октября 10:00-11:30 – Zoom \n\n"\
        + "<b>Внутренняя система оценки качества образования ИТМО (2 ак.ч)</b>\n" \
        + "Преподаватель: Тишкина К.О\n" \
        + "1. 17 октября 11:40-13:10 – Zoom\n" \
        + "2. 18 октября 15:20-16:50 – Zoom\n\n"\
        + "<b>Барс 2.0. Как применять (2 ак.ч)</b>\n" \
        + "Преподаватель: Джавлах Е.С., Токарева А.А\n" \
        + "1. 15 октября 17:00-18:30 – Zoom\n" \
        + "2. 18 октября 17:00-18:30 – Zoom\n\n"\
        + "<b>Педагогический дизайн (2 ак.ч.)</b>\n" \
        + "Преподаватель: Казанцева М.В.\n" \
        + "1. 18 октября 11:40-13:10 – Zoom \n" \
        + "Преподаватель: Шестакова Е.С.\n" \
        + "2. 18 октября 18:40-20:10 – Zoom \n\n"\
        + "<b>Современные образовательные технологии (3 ак.ч.)</b>\n" \
        + "Преподаватель: Шпарберг А. Л.\n" \
        + "1. 18 октября 10:00-12:00 – Zoom\n\n" \
        + "⚡️ <u>Занятия, которые состоятся на неделе <b>21.10 - 25.10</b></u>:\n\n" \
        + "<b>Адаптация иностранных студентов в образовательном процессе (2 ак.ч.)</b>\n" \
        + "Преподаватель: Кондрашова Н.В. \n" \
        + "1. 21 октября 17:00-18:30 – Zoom \n\n"\
        + "<b>Современные образовательные технологии (3 ак.ч.)</b>\n" \
        + "Преподаватель: Шпарберг А. Л.\n" \
        + "1. 23 октября 15:00-17:00 – Zoom\n\n"\
        + "<b>Техническое оснащение аудиторий ИТМО (2 ак.ч)</b>\n" \
        + "Преподаватель: Новожилов А.С.\n" \
        + "1. 22 октября 11:40-13:10 – ул. Ломоносова, д.9., ауд. 1122\n" \
        + "2. 25 октября 17:00-18:30 – Кронверкский, д.49., ауд. 1419\n\n"\
        + "<b>Воркшоп. Правила педагогической коммуникации (2 ак.ч)</b>\n" \
        + "Преподаватель: Никуленко А. А.\n" \
        + "1. 22 октября 17:00-18:30 – Zoom \n" \
        + "2. 24 октября 10:00-11:30 – Zoom\n",
            reply_markup=get_user_sign_or_quit_practice_kb(),
    )

    await state.clear()
