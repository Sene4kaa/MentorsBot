import psycopg

from aiogram.exceptions import TelegramBadRequest
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from django.conf import settings

from bot.services.keyboards import get_start_admin_menu_kb, get_start_user_kb, get_menu_kb, get_user_registration_kb
from bot.services.messages import get_start_user_mes

router = Router()

AdminList = settings.ADMINS
DATABASE_URL = settings.DATABASE_URL

# Получение айди пользователя
@router.message(Command("start1"))
async def cmd_start(message: types.Message):
    await message.answer(str(message.from_user.id))


# Приветственное сообщение
@router.message(Command(commands=["start"]))
async def cmd_start(message: types.Message, state: FSMContext):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            await state.clear()

            if str(message.from_user.id) not in AdminList:
                sql = """SELECT user_id FROM users"""
                list = cursor.execute(sql).fetchall()
                user_id_list = []
                for user in list:
                    user_id_list.append(user[0])

                if message.from_user.id not in user_id_list:
                    await message.answer(
                        text="Вам необходимо зарегистрироваться.", reply_markup=get_user_registration_kb()
                    )
                else:
                    content = get_start_user_mes()

                    await message.answer(**content.as_kwargs(), reply_markup=get_start_user_kb())

            else:
                await message.answer("Меню", reply_markup=get_start_admin_menu_kb())

            cursor.execute(
                """INSERT INTO last_bot_message (user_id, message_number) VALUES (%s, %s)""",
                [message.from_user.id, message.message_id],
            )

            conn.commit()
            await message.delete()


@router.callback_query(default_state, F.data == "CancelAdminOperation")
async def cmd_cancel_no_state(callback: CallbackQuery, state: FSMContext):

    await state.set_data({})
    await callback.message.edit_text(text="Меню", reply_markup=get_start_admin_menu_kb())


@router.callback_query(F.data == "CancelAdminOperation")
async def cmd_cancel_admin(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text="Меню", reply_markup=get_start_admin_menu_kb())


@router.callback_query(default_state, F.data == "CancelUserOperation")
async def cmd_cancel_no_state(callback: CallbackQuery, state: FSMContext):

    await state.set_data({})
    await callback.message.edit_text(
        text="<b>Меню</b>\n\n"
        + "<b>🗺 Дорожная карта</b> - здесь можно посмотреть дорожную карту всего курса. "
        + "<i>Cохрани</i> ее себе, чтобы она всегда была под рукой 🙌\n\n"

        + "<b>📚 Занятия</b> - здесь можно <i>записаться</i> на <b>занятия</b>."
        + "\nЗдесь же можно отписаться от занятия, посмотреть текущие записи и "
        + "получить номера аудиторий или ссылки для подключения 👀\n\n"

        + "<b>⚙️ Мастерские</b> - здесь можно <i>записаться</i> на <b>мастерские</b>."
        + "\nЗдесь же можно отписаться от мастерской, посмотреть текущие записи и "
        + "получить номера аудиторий или ссылки для подключения 👨‍💻\n\n"

        + "<b>📝 Оставить обратную связь</b> - здесь можно поставить оценку занятию или поделиться впечатлениями о нем\n"

        + "\n<b>📣 Связаться с нами</b> - здесь можно получить контакты организаторов и задать им вопрос напрямую\n\n"
        + "Выбери то, что тебя интересует <i>прямо сейчас</i>:",
        reply_markup=get_menu_kb(),
    )


@router.callback_query(F.data == "CancelUserOperation")
async def cmd_cancel_user(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text="<b>Меню</b>\n\n"
             + "<b>🗺 Дорожная карта</b> - здесь можно посмотреть дорожную карту всего курса. "
             + "<i>Cохрани</i> ее себе, чтобы она всегда была под рукой 🙌\n\n"

             + "<b>📚 Занятия</b> - здесь можно <i>записаться</i> на <b>занятия</b>."
             + "\nЗдесь же можно отписаться от занятия, посмотреть текущие записи и "
             + "получить номера аудиторий или ссылки для подключения 👀\n\n"

             + "<b>⚙️ Мастерские</b> - здесь можно <i>записаться</i> на <b>мастерские</b>."
             + "\nЗдесь же можно отписаться от мастерской, посмотреть текущие записи и "
             + "получить номера аудиторий или ссылки для подключения 👨‍💻\n\n"

             + "<b>📝 Оставить обратную связь</b> - здесь можно поставить оценку занятию или поделиться впечатлениями о нем\n"

             + "\n<b>📣 Связаться с нами</b> - здесь можно получить контакты организаторов и задать им вопрос напрямую\n\n"
             + "Выбери то, что тебя интересует <i>прямо сейчас</i>:",
        reply_markup=get_menu_kb(),
    )


@router.callback_query(default_state, F.data == "CancelUserRegistration")
async def cmd_cancel_no_state(callback: CallbackQuery, state: FSMContext):

    await state.set_data({})
    await callback.message.edit_text(text="Вам необходимо зарегистрироваться.", reply_markup=get_user_registration_kb())


@router.callback_query(F.data == "CancelUserRegistration")
async def cmd_cancel_user(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text="Вам необходимо зарегистрироваться.", reply_markup=get_user_registration_kb())
