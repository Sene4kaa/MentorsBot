from aiogram import types, F, Router

from services.keyboards import get_menu_kb


router = Router()


# Меню
@router.callback_query(F.data == "menu1")
async def send_menu(callback: types.CallbackQuery):

    await callback.message.edit_text(
        text="<b>Меню</b>\n\n" +
             "<b>🗺 Дорожная карта</b> - здесь можно посмотреть дорожную карту всего курса. <i>Cохрани</i> ее себе, чтобы она всегда была под рукой 🙌\n\n" + 
             "<b>📚 Занятия</b> - здесь можно <i>записаться</i> на <b>занятия</b>.\nЗдесь же можно отписаться от занятия, посмотреть текущие записи и получить номера аудиторий или ссылки для подключения 👀\n\n" +
             "<b>⚙️ Мастерские</b> - здесь можно <i>записаться</i> на <b>мастерские</b>.\nЗдесь же можно отписаться от мастерской, посмотреть текущие записи и получить номера аудиторий или ссылки для подключения 👨‍💻\n\n" + 
             "<b>📝 Оставить обратную связь</b> - здесь можно поставить оценку занятию или поделиться впечатлениями о нем\n\n" + 
             "<b>📣 Связаться с нами</b> - здесь можно получить контакты организаторов и задать им вопрос напрямую\n\n" +
             "Выбери то, что тебя интересует <i>прямо сейчас</i>:", 
        reply_markup=get_menu_kb()
    )

# Меню
@router.callback_query(F.data == "menu")
async def send_menu(callback: types.CallbackQuery):

    await callback.message.edit_text(
        text="<b>Меню</b>\n\n" +
             "<b>🗺 Дорожная карта</b> - здесь можно посмотреть дорожную карту всего курса. <i>Cохрани</i> ее себе, чтобы она всегда была под рукой 🙌\n\n" + 
             "<b>📚 Занятия</b> - здесь можно <i>записаться</i> на <b>занятия</b>.\nЗдесь же можно отписаться от занятия, посмотреть текущие записи и получить номера аудиторий или ссылки для подключения 👀\n\n" +
             "<b>⚙️ Мастерские</b> - здесь можно <i>записаться</i> на <b>мастерские</b>.\nЗдесь же можно отписаться от мастерской, посмотреть текущие записи и получить номера аудиторий или ссылки для подключения 👨‍💻\n\n" + 
             "<b>📝 Оставить обратную связь</b> - здесь можно поставить оценку занятию или поделиться впечатлениями о нем\n\n" + 
             "<b>📣 Связаться с нами</b> - здесь можно получить контакты организаторов и задать им вопрос напрямую\n\n" +
             "Выбери то, что тебя интересует <i>прямо сейчас</i>:", 
        reply_markup=get_menu_kb()
    )
