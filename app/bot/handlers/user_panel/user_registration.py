import psycopg
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from django.conf import settings

from bot.services.keyboards import get_user_finish_registration_kb, get_back_to_user_menu_kb
from bot.services.messages import get_after_registraion_user_mes

DATABASE_URL = settings.DATABASE_URL


class Registration(StatesGroup):
    entering_surname = State()
    entering_name = State()
    accepting = State()


router = Router()


@router.callback_query(StateFilter(None), F.data == "UserRegistration")
async def user_registration_started(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text(text="Введите вашу фамилию")
    await state.update_data(bot_surname_message=callback.message.message_id)
    await state.set_state(Registration.entering_surname)


@router.message(Registration.entering_surname)
async def surname_entered(message: Message, state: FSMContext):

    surname = message.text
    await state.update_data(surname_message=message.message_id)
    await state.update_data(user_surname=surname)

    await message.answer(text="Введите ваше имя")
    await state.set_state(Registration.entering_name)
    await state.update_data(bot_name_message=message.message_id + 1)


@router.message(Registration.entering_name)
async def name_entered(message: Message, state: FSMContext):

    name = message.text
    await state.update_data(name_message=message.message_id)
    await state.update_data(user_id=message.from_user.id)
    await state.update_data(chat_id=message.chat.id)
    await state.update_data(user_name=name)
    user_data = await state.get_data()

    await message.answer(
        text=f"Вас зовут {user_data['user_name']} {user_data['user_surname']} ?",
        reply_markup=get_user_finish_registration_kb(),
    )

    await message.bot.delete_messages(
        chat_id=message.chat.id,
        message_ids=[
            user_data["bot_surname_message"],
            user_data["surname_message"],
            user_data["bot_name_message"],
            user_data["name_message"],
        ],
    )

    await state.set_state(Registration.accepting)


@router.callback_query(Registration.accepting)
async def accepted_registration(callback: CallbackQuery, state: FSMContext):

    user_data = await state.get_data()

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            sql = """INSERT INTO users (user_id, chat_id, name, surname) VALUES (%s, %s, %s, %s)"""
            cursor.execute(
                sql, (user_data["user_id"], user_data["chat_id"], user_data["user_name"], user_data["user_surname"])
            )
            conn.commit()

    content = get_after_registraion_user_mes()
    await callback.message.edit_text(
        **content.as_kwargs(),
        reply_markup=get_back_to_user_menu_kb(),
    )

    await state.clear()
