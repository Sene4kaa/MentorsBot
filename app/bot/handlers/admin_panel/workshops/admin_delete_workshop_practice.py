import psycopg
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from django.conf import settings

from bot.services.keyboards import get_admin_list_kb, delete_admin_practice_kb, get_back_to_admin_menu_kb
from bot.services.messages import get_workshops_name_list, get_workshops_format_list, get_deleting_workshops_list

DATABASE_URL = settings.DATABASE_URL


class DeleteWorkshop(StatesGroup):
    choosing_workshop_name = State()
    choosing_workshop_format = State()
    ending_deleting_workshop = State()
    back_to_menu = State()


router = Router()


@router.callback_query(StateFilter(None), F.data == "DeleteWorkshopPractice")
async def deleting_workshop_name_chosen(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        text="Выберите занятие для удаления:", reply_markup=get_admin_list_kb(set(get_workshops_name_list()))
    )

    await state.set_state(DeleteWorkshop.choosing_workshop_name)


@router.callback_query(DeleteWorkshop.choosing_workshop_name)
async def deleting_workshop_format_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_name=callback.data)

    await callback.message.edit_text(
        text="Выберите формат занятия:", reply_markup=get_admin_list_kb(set(get_workshops_format_list(callback.data)))
    )

    await state.set_state(DeleteWorkshop.choosing_workshop_format)


@router.callback_query(DeleteWorkshop.choosing_workshop_format)
async def deleting_workshop_list_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_format=callback.data)

    user_data = await state.get_data()

    await callback.message.edit_text(
        text="Выберите время занятия:",
        reply_markup=get_admin_list_kb(
            set(get_deleting_workshops_list(user_data["chosen_name"], user_data["chosen_format"]))
        ),
    )

    await state.set_state(DeleteWorkshop.ending_deleting_workshop)


@router.callback_query(DeleteWorkshop.ending_deleting_workshop)
async def deleting_workshop(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_time=callback.data)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Подтвердите удаление занятия:\n{user_data['chosen_name']}, {user_data['chosen_format']}, {user_data['chosen_time']}?",
        reply_markup=delete_admin_practice_kb(),
    )

    await state.set_state(DeleteWorkshop.back_to_menu)


@router.callback_query(DeleteWorkshop.back_to_menu)
async def end_deleting_workshop(callback: CallbackQuery, state: FSMContext):

    user_data = await state.get_data()

    print(user_data["chosen_time"].split(", "))
    sql = """DELETE FROM workshops_schedule WHERE title=%s AND format=%s AND date=%s AND hours=%s AND minutes=%s"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    user_data["chosen_name"],
                    user_data["chosen_format"],
                    user_data["chosen_time"].split(", ")[0] + ", " + user_data["chosen_time"].split(", ")[1],
                    user_data["chosen_time"].split(", ")[2][:2],
                    user_data["chosen_time"].split(", ")[2][3:],
                ),
            )

            conn.commit()

    await callback.message.edit_text(text="Занятие успешно удалено!", reply_markup=get_back_to_admin_menu_kb())

    await state.clear()
