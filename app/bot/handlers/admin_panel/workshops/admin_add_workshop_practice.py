import psycopg
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import types, F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from django.conf import settings

from bot.services.keyboards import (
    get_admin_list_kb,
    get_save_workshop_kb,
    get_back_to_admin_menu_kb,
    get_admin_number_list_kb,
)

DATABASE_URL = settings.DATABASE_URL


class Workshop(StatesGroup):
    choosing_workshop_name = State()
    choosing_workshop_format = State()
    choosing_workshop_month = State()
    choosing_workshop_day = State()
    choosing_workshop_hour = State()
    choosing_workshop_minute = State()
    additional_info = State()
    saving_workshop = State()


def get_all_lessons_list():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM workshops_title")
            titles_list = []
            titles = cursor.fetchall()
    for x in titles:
        titles_list.append(x[0])

    return titles_list


router = Router()

titles_list = get_all_lessons_list()

available_workshop_formats = ["Zoom", "Очно, Кронверкский", "Очно, Ломоносова"]
available_workshop_months = ["Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
available_workshop_day = [str(x) for x in range(1, 32)]
available_workshop_hour = ["08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"]
available_workshop_minute = ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]


@router.callback_query(StateFilter(None), F.data == "AddWorkshopPractice")
async def add_workshop(callback: types.CallbackQuery, state: FSMContext):

    titles_list = get_all_lessons_list()

    await callback.message.edit_text(
        text="Выберите занятие для добавления:", reply_markup=get_admin_list_kb(set(titles_list))
    )
    await state.set_state(Workshop.choosing_workshop_name)


@router.callback_query(Workshop.choosing_workshop_name)
async def workshop_name_chosen(callback: CallbackQuery, state: FSMContext):
    await state.update_data(chosen_workshop=callback.data)

    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Вы выбрали {user_data['chosen_workshop']}.\n\nТеперь введите формат:",
        reply_markup=get_admin_list_kb(available_workshop_formats),
    )
    await state.set_state(Workshop.choosing_workshop_format)


@router.callback_query(Workshop.choosing_workshop_format, F.data.in_(available_workshop_formats))
async def workshop_format_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_format=callback.data)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Вы выбрали {user_data['chosen_workshop']}, {user_data['chosen_format']}.\n\nТеперь выберите месяц",
        reply_markup=get_admin_list_kb(available_workshop_months),
    )

    await state.set_state(Workshop.choosing_workshop_month)


@router.callback_query(Workshop.choosing_workshop_month, F.data.in_(available_workshop_months))
async def workshop_month_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_month=callback.data)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Вы выбрали {user_data['chosen_workshop']}, {user_data['chosen_format']}, {user_data['chosen_month']}."
        + "\n\nТеперь выберите день:",
        reply_markup=get_admin_number_list_kb(available_workshop_day),
    )

    await state.set_state(Workshop.choosing_workshop_day)


@router.callback_query(Workshop.choosing_workshop_day, F.data.in_(available_workshop_day))
async def workshop_day_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_day=callback.data)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Вы выбрали {user_data['chosen_workshop']}, {user_data['chosen_format']}, "
        + f"{user_data['chosen_month']}, {user_data['chosen_day']}."
        + "\n\nТеперь выберите час:",
        reply_markup=get_admin_number_list_kb(available_workshop_hour),
    )

    await state.set_state(Workshop.choosing_workshop_hour)


@router.callback_query(Workshop.choosing_workshop_hour, F.data.in_(available_workshop_hour))
async def workshop_hour_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_hour=callback.data)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Вы выбрали {user_data['chosen_workshop']}, {user_data['chosen_format']}, "
        + f"{user_data['chosen_month']}, {user_data['chosen_day']}, {user_data['chosen_hour']}"
        + "\n\nТеперь выберите минуты:",
        reply_markup=get_admin_number_list_kb(available_workshop_minute),
    )

    await state.set_state(Workshop.choosing_workshop_minute)


@router.callback_query(Workshop.choosing_workshop_minute, F.data.in_(available_workshop_minute))
async def workshop_hour_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_minute=callback.data)
    user_data = await state.get_data()

    if user_data["chosen_format"] == "Zoom":
        await callback.message.edit_text(
            text=f"Вы выбрали: \nПредмет: {user_data['chosen_workshop']}\nФормат: {user_data['chosen_format']}"
            + f"\nДата: {user_data['chosen_day']}, {user_data['chosen_month']}\n"
            + f"Время: {user_data['chosen_hour']}:{user_data['chosen_minute']}\n\nПрикрепите ссылку на Zoom:",
        )
    else:
        await callback.message.edit_text(
            text=f"Вы выбрали: \nПредмет: {user_data['chosen_workshop']}\nФормат: {user_data['chosen_format']}"
            + f"\nДата: {user_data['chosen_day']}, {user_data['chosen_month']}\n"
            + f"Время: {user_data['chosen_hour']}:{user_data['chosen_minute']}\n\nНапишите номер аудитории:",
        )

    await state.set_state(Workshop.additional_info)


@router.message(Workshop.additional_info)
async def practice_additional_info(message: Message, state: FSMContext):

    answer = message.text
    await state.update_data(add_info=answer)
    user_data = await state.get_data()
    await message.delete()
    if user_data["chosen_format"] == "Zoom":

        await message.answer(
            text=f"Вы выбрали:\nПредмет: {user_data['chosen_workshop']}\nФормат: {user_data['chosen_format']}"
            + f"\nДата: {user_data['chosen_day']}, {user_data['chosen_month']}\n"
            + f"Время: {user_data['chosen_hour']}:{user_data['chosen_minute']}\nСсылка на Zoom: {user_data['add_info']}",
            reply_markup=get_save_workshop_kb(),
        )
    else:

        await message.answer(
            text=f"Вы выбрали:\nПредмет: {user_data['chosen_workshop']}\nФормат: {user_data['chosen_format']}"
            + f"\nДата: {user_data['chosen_day']}, {user_data['chosen_month']}\n"
            + f"Время: {user_data['chosen_hour']}:{user_data['chosen_minute']}\nНомер аудитории: {user_data['add_info']}",
            reply_markup=get_save_workshop_kb(),
        )


@router.callback_query(F.data == "save_workshop")
async def saving_workshop(callback: CallbackQuery, state: FSMContext):

    user_data = await state.get_data()

    sql = """INSERT INTO workshops_schedule 
            (title, format, date, hours, minutes, users_number, additional_info) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    user_data["chosen_workshop"],
                    user_data["chosen_format"],
                    user_data["chosen_day"] + ", " + user_data["chosen_month"],
                    user_data["chosen_hour"],
                    user_data["chosen_minute"],
                    0,
                    user_data["add_info"],
                ),
            )
            conn.commit()
    await callback.message.edit_text(text="Мастерская успешно добавлена!", reply_markup=get_back_to_admin_menu_kb())

    await state.clear()
