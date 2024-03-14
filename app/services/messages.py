import psycopg
from aiogram.utils.formatting import Bold, as_list, as_marked_section

from config import DATABASE_URL


def get_lessons_names():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM lessons_title")
            titles_list = []
            titles = cursor.fetchall()
            for x in titles:
                titles_list.append(str(x[0]))

            return titles_list


def get_workshops_names():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM workshops_title")
            titles_list = []
            titles = cursor.fetchall()
            for x in titles:
                titles_list.append(str(x[0]))

            return titles_list


def get_lessons_name_list():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM schedule")
            titles_list = []
            titles = cursor.fetchall()
            for x in titles:
                titles_list.append(str(x[0]))

            return titles_list


def get_workshops_name_list():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM workshops_schedule")
            titles_list = []
            titles = cursor.fetchall()
            for x in titles:
                titles_list.append(str(x[0]))

            return titles_list


def get_lessons_lower_35_list(user_id):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            user_list = cursor.execute("SELECT lessons FROM practices WHERE user_id=%s ", [user_id]).fetchall()
            cursor.execute("SELECT DISTINCT lesson FROM schedule WHERE users_number < 35")

            titles_list = []
            titles = cursor.fetchall()
            for x in titles:
                if x not in user_list:
                    titles_list.append(str(x[0]))

            return titles_list


def get_workshops_lower_35_list(user_id):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            user_list = cursor.execute("SELECT title FROM workshops WHERE user_id=%s ", [user_id]).fetchall()
            cursor.execute("SELECT DISTINCT title FROM workshops_schedule WHERE users_number < 35")

            titles_list = []
            titles = cursor.fetchall()
            for x in titles:
                if x not in user_list:
                    titles_list.append(str(x[0]))

            return titles_list


def get_lessons_with_user_id(user_id):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            user_list = cursor.execute("SELECT lessons FROM practices WHERE user_id=%s ", [user_id]).fetchall()

            titles_list = []
            for x in user_list:
                titles_list.append(str(x[0]))

            return titles_list


def get_workshops_with_user_id(user_id):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            user_list = cursor.execute("SELECT title FROM workshops WHERE user_id=%s ", [user_id]).fetchall()

            titles_list = []
            for x in user_list:
                titles_list.append(str(x[0]))

            return titles_list


def get_lessons_format_list(name):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM schedule where lesson=%s""", [name])
            title_list = []
            titles = cursor.fetchall()
            for x in titles:
                title_list.append(str(x[1]))

            return title_list


def get_workshops_format_list(name):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM workshops_schedule where title=%s""", [name])
            title_list = []
            titles = cursor.fetchall()
            for x in titles:
                title_list.append(str(x[1]))

            return title_list


def get_deleting_lessons_list(data1, data2):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM schedule where lesson=%s and format=%s""", (data1, data2))
            title_list = []
            titles = cursor.fetchall()
            for x in titles:
                title_list.append(str(x[2]) + ", " + str(x[3]) + ":" + str(x[4]))

            return title_list


def get_deleting_workshops_list(data1, data2):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT DISTINCT * FROM workshops_schedule where title=%s and format=%s""", (data1, data2)
            )
            title_list = []
            titles = cursor.fetchall()
            for x in titles:
                title_list.append(str(x[2]) + ", " + str(x[3]) + ":" + str(x[4]))

            return title_list


def get_start_user_mes():
    content = as_list(
        "Приветствуем тебя, дорогой ментор!\n",
        as_marked_section(
            "В этом боте ты можешь:\n",
            " Записаться на занятия или мастерские",
            " Посмотреть расписание",
            " Получить ссылки для подключения",
            " Оставить обратную связь",
            " Связаться с организаторами",
            marker="✅",
        ),
        "\n\nНажми ",
        Bold("меню"),
        ", чтобы продолжить",
        sep="",
    )

    return content


def get_lessons_list_mes(lessons):

    lessons = "\n".join(lessons)
    content = f"Ваши тренинги:\n{lessons}"
    return content


def get_after_registraion_user_mes():
    content = as_list(
        "Регистрация прошла успешно!\n\nДорогой ментор!",
        as_marked_section(
            " В этом боте ты можешь:\n",
            " Записаться на занятия или мастерские",
            " Посмотреть расписание",
            " Получить информацию о занятиях",
            " Оставить обратную связь",
            " Связаться с организаторами",
            marker="✅",
        ),
        "\n\nНажмите ",
        Bold("меню"),
        ", чтобы продолжить",
        sep="",
    )

    return content
