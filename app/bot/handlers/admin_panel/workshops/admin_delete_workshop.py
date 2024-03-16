import psycopg
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram import F, Router
from aiogram.types import CallbackQuery
from django.conf import settings

from bot.services.keyboards import get_admin_list_kb, get_back_to_admin_menu_kb, delete_admin_practice_kb
from bot.services.messages import get_workshops_names

DATABASE_URL = settings.DATABASE_URL


class DeletingWorkshop(StatesGroup):

    choosing_workshop = State()
    deleting_workshop = State()


router = Router()


@router.callback_query(StateFilter(None), F.data == "DeleteWorkshop")
async def start_deleting_workshop(callback: CallbackQuery, state: FSMContext):

    titles_list = get_workshops_names()

    await callback.message.edit_text(
        text="Выберите предмет для удаления", reply_markup=get_admin_list_kb(set(titles_list))
    )

    await state.set_state(DeletingWorkshop.choosing_workshop)


@router.callback_query(DeletingWorkshop.choosing_workshop)
async def workshop_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_workshop=callback.data)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Вы хотите удалить {user_data['chosen_workshop']}?", reply_markup=delete_admin_practice_kb()
    )

    await state.set_state(DeletingWorkshop.deleting_workshop)


@router.callback_query(DeletingWorkshop.deleting_workshop)
async def ending_deleting_workshop(callback: CallbackQuery, state: FSMContext):

    await state.update_data(choice=callback.data)
    user_data = await state.get_data()

    sql_admin = """DELETE FROM workshops_title WHERE title=%s"""
    sql_user = """DELETE FROM workshops WHERE title=%s"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_admin, [user_data["chosen_workshop"]])
            cursor.execute(sql_user, [user_data["chosen_workshop"]])
            conn.commit()

    await callback.message.edit_text(
        text=f"Предмет {user_data['chosen_workshop']} успешно удален!", reply_markup=get_back_to_admin_menu_kb()
    )

    await state.clear()
