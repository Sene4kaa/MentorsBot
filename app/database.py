import psycopg

from config import DATABASE_URL

conn = psycopg.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS schedule
       (lesson text, format text, date text, hours text, minutes text, users_number integer, additional_info text)"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS users
       (user_id integer, chat_id integer, name text, surname text)"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS practices
       (user_id integer, lessons text, format text, date text, hours text, minutes text)"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS lessons_title (title text)"""
)
cursor.execute(
    """CREATE TABLE IF NOT EXISTS quited_practice (practice text, reason text)"""
)
cursor.execute(
    """CREATE TABLE IF NOT EXISTS last_bot_message (user_id integer, message_number integer)"""
)
cursor.execute(
    """CREATE TABLE IF NOT EXISTS workshops_schedule 
    (title text, format text, date text, hours text, minutes text, users_number integer, additional_info text)"""
)
cursor.execute(
    """CREATE TABLE IF NOT EXISTS workshops 
    (user_id integer, title text, format text, date text, hours text, minutes text)"""
)
cursor.execute(
    """CREATE TABLE IF NOT EXISTS workshops_title 
    (title text)"""
)
cursor.execute(
    """CREATE TABLE IF NOT EXISTS quited_workshops (workshop text, reason text)"""
)

conn.commit()
