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

    sql_admin_1 = """SELECT * FROM workshops"""
    sql_admin_2 = """SELECT * FROM users"""
    sql_admin_3 = """SELECT * FROM workshops_schedule"""
    sql_admin_4 = """SELECT * FROM workshops_title"""
    sql_admin_5 = """UPDATE schedule SET date = '2, Май', hours = 15, minutes = 20, 
    additional_info = 'https://itmo.zoom.us/j/86470855052?pwd=ZlZLNzF3S0t5N0dWbm80OVRzdkFXdz09'
    WHERE lesson = 'Активное обучение'"""

    sql_admin_6 = """UPDATE practices SET date = '2, Май', hours = 15, minutes = 20 
    WHERE lessons = 'Активное обучение'"""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            msg = cursor.execute(sql_admin_1).fetchall()
            user = cursor.execute(sql_admin_2).fetchall()
            schedule = cursor.execute(sql_admin_3).fetchall()
            titles = cursor.execute(sql_admin_4).fetchall()

            cursor.execute(sql_admin_5)
            cursor.execute(sql_admin_6)
            conn.commit()

    answer = ''
    for x in msg:
        for y in x:
            answer += str(y) + ', '
        answer += '\n'
    if answer != '':
        await callback.message.edit_text(text=answer)

    answer = ''
    for x in user:
        for y in x:
            answer += str(y) + ', '
        answer += '\n'
    if answer != '':
        await callback.message.answer(
            text=answer
        )

    answer = ''
    for x in schedule:
        for y in x:
            answer += str(y) + ', '
        answer += '\n'
    if answer != '':
        await callback.message.answer(
            text=answer
        )

    answer = ''
    for x in titles:
        for y in x:
            answer += str(y) + ', '
        answer += '\n'
    if answer != '':
        await callback.message.answer(
            text=answer,
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
