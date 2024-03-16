from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.services.keyboards import get_roadmap_kb


router = Router()


@router.callback_query(F.data == "roadmap")
async def send_roadmap(callback: CallbackQuery):

    await callback.message.edit_text(
        text="<b>Дорожная карта</b>\n\nЗдесь можно посмотреть дорожную карту всего курса.\n"
        + "Карта может пополняться и корректироваться, актуальная версия всегда находится <i>в этом разделе</i> 😌\n\n"
        + "Сохрани ее себе, чтобы она всегда была под рукой 🤝\n\n"
        + "Если вам удобно смотреть расписание всех занятий в режиме <i>таймлайна</i>, переходите в наш miro.",
        reply_markup=get_roadmap_kb(),
    )
