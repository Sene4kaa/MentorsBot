import psycopg
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from config import DATABASE_URL
from services.messages import get_lessons_name_list, get_lessons_format_list, get_deleting_lessons_list
from services.keyboards import get_admin_list_kb, delete_admin_practice_kb, get_back_to_admin_menu_kb


class CheckStudents(StatesGroup):
    choosing_practice_name = State()
    choosing_practice_format = State()
    choosing_practice_time = State()
    accepting = State()


router = Router()


@router.callback_query(StateFilter(None), F.data == "CheckStudents")
async def start_checking_students(callback: CallbackQuery, state: FSMContext):

    practices = get_lessons_name_list()

    await callback.message.edit_text(text="Выберите занятие", reply_markup=get_admin_list_kb(set(practices)))
    await state.set_state(CheckStudents.choosing_practice_name)


@router.callback_query(CheckStudents.choosing_practice_name)
async def practice_name_chosen(callback: CallbackQuery, state: FSMContext):

    formats = get_lessons_format_list(callback.data)
    await state.update_data(chosen_practice=callback.data)

    await callback.message.edit_text(
        text=f"Вы выбрали занятие {callback.data}.\n\nВыберите формат", reply_markup=get_admin_list_kb(set(formats))
    )
    await state.set_state(CheckStudents.choosing_practice_format)


@router.callback_query(CheckStudents.choosing_practice_format)
async def practice_format_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_format=callback.data)
    user_data = await state.get_data()

    times = get_deleting_lessons_list(user_data["chosen_practice"], user_data["chosen_format"])
    await callback.message.edit_text(
        text=f"Вы выбрали\nПредмет: {user_data['chosen_practice']}\nФормат: {user_data['chosen_format']}.\n\nВыберите время",
        reply_markup=get_admin_list_kb(set(times)),
    )
    await state.set_state(CheckStudents.choosing_practice_time)


@router.callback_query(CheckStudents.choosing_practice_time)
async def practice_time_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_time=callback.data)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Вы выбрали\nПредмет: {user_data['chosen_practice']}\nФормат: {user_data['chosen_format']}\n"
        + f"Время: {user_data['chosen_time']}\n\n Подтвердите.",
        reply_markup=delete_admin_practice_kb(),
    )
    await state.set_state(CheckStudents.accepting)


@router.callback_query(CheckStudents.accepting)
async def practice_chosen(callback: CallbackQuery, state: FSMContext):

    user_data = await state.get_data()

    sql_schedule = """SELECT user_id FROM practices WHERE
                      lessons = %s AND format = %s AND date = %s AND hours = %s AND minutes = %s"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            tuple_user_ids = cursor.execute(
                sql_schedule,
                [
                    user_data["chosen_practice"],
                    user_data["chosen_format"],
                    user_data["chosen_time"].split(", ")[0] + ", " + user_data["chosen_time"].split(", ")[1],
                    user_data["chosen_time"].split(", ")[2][:2],
                    user_data["chosen_time"].split(", ")[2][3:],
                ],
            ).fetchall()

            user_ids = []
            for user in tuple_user_ids:
                user_ids.append(user[0])
            sql_users = """SELECT surname, name FROM users WHERE user_id IN ({0})""".format(
                ", ".join("%s" for _ in user_ids)
            )
            names = cursor.execute(sql_users, user_ids).fetchall()

    names_number = len(names)
    names_surnames = []
    for user in names:
        names_surnames.append(user[0] + " " + user[1])

    names = "\n".join(names_surnames)

    await callback.message.edit_text(
        text=f"Всего участников: {names_number}.\nСписок участников:\n{names}", reply_markup=get_back_to_admin_menu_kb()
    )
    await state.clear()
