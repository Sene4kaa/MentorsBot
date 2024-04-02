import psycopg
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram import F, Router
from aiogram.types import CallbackQuery
from django.conf import settings

from bot.services.keyboards import get_admin_list_kb, get_back_to_admin_menu_kb, delete_admin_practice_kb
from bot.services.messages import get_lessons_names

DATABASE_URL = settings.DATABASE_URL


class DeletingLesson(StatesGroup):

    choosing_lesson = State()
    deleting_lesson = State()


router = Router()


@router.callback_query(F.data == "ClearPractices")
async def clear_practices(callback: CallbackQuery):

    sql_admin_1 = """UPDATE workshops_schedule SET users_number = 13 
                   WHERE title = 'Дизайн учебных презентаций' AND date = '12, Апрель'"""
    sql_admin_2 = """UPDATE workshops_schedule SET users_number = 8 
                       WHERE title = 'Оценивание' AND date = '9, Апрель'"""
    sql_admin_3 = """UPDATE workshops_schedule SET users_number = 5 
                       WHERE title = 'Адаптация уч.материалов' AND date = '1, Апрель'"""
    sql_admin_4 = """UPDATE workshops_schedule SET users_number = 7 
                           WHERE title = 'Разработка занятия' AND date = '15, Апрель'"""
    sql_admin_5 = """UPDATE workshops_schedule SET users_number = 10 
                           WHERE title = 'Практики пед.общения и мотивация' AND date = '5, Апрель'"""

    sql_admin_6 = """UPDATE schedule SET users_number = 20 
                               WHERE lesson = 'Управление эмоциями в уч.среде' AND date = '2, Апрель'"""
    sql_admin_7 = """UPDATE schedule SET users_number = 15 
                               WHERE lesson = 'Управление эмоциями в уч.среде' AND date = '4, Апрель'"""
    sql_admin_8 = """UPDATE schedule SET users_number = 7 
                               WHERE lesson = 'Практикум пед.наблюдения' AND date = '4, Апрель'"""
    sql_admin_9 = """UPDATE schedule SET users_number = 9 
                               WHERE lesson = 'Практикум пед.наблюдения' AND date = '10, Апрель'"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_admin_1)
            cursor.execute(sql_admin_2)
            cursor.execute(sql_admin_3)
            cursor.execute(sql_admin_4)
            cursor.execute(sql_admin_5)
            cursor.execute(sql_admin_6)
            cursor.execute(sql_admin_7)
            cursor.execute(sql_admin_8)
            cursor.execute(sql_admin_9)

            conn.commit()

    await callback.message.edit_text(
        text="Данные обновлены! :):):):):):)):):)",
        reply_markup=get_back_to_admin_menu_kb()
    )


@router.callback_query(StateFilter(None), F.data == "DeleteLesson")
async def start_deleting_lesson(callback: CallbackQuery, state: FSMContext):

    titles_list = get_lessons_names()

    await callback.message.edit_text(
        text="Выберите предмет для удаления", reply_markup=get_admin_list_kb(titles_list)
    )

    await state.set_state(DeletingLesson.choosing_lesson)


@router.callback_query(DeletingLesson.choosing_lesson)
async def lesson_chosen(callback: CallbackQuery, state: FSMContext):

    await state.update_data(chosen_lesson=callback.data)
    user_data = await state.get_data()

    await callback.message.edit_text(
        text=f"Вы хотите <u>окончательно</u> удалить\n<b>{user_data['chosen_lesson']}</b>?",
        reply_markup=delete_admin_practice_kb()
    )

    await state.set_state(DeletingLesson.deleting_lesson)


@router.callback_query(DeletingLesson.deleting_lesson)
async def ending_deleting_lesson(callback: CallbackQuery, state: FSMContext):

    await state.update_data(choice=callback.data)
    user_data = await state.get_data()

    sql_admin = """DELETE FROM lessons_title WHERE title=%s"""
    sql_user = """DELETE FROM practices WHERE lessons=%s"""
    sql_admin_lesson = """DELETE FROM schedule WHERE lesson=%s"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_admin, [user_data["chosen_lesson"]])
            cursor.execute(sql_user, [user_data["chosen_lesson"]])
            cursor.execute(sql_admin_lesson, [user_data["chosen_lesson"]])
            conn.commit()

    await callback.message.edit_text(
        text=f"Предмет {user_data['chosen_lesson']} успешно удален!", reply_markup=get_back_to_admin_menu_kb()
    )

    await state.clear()
