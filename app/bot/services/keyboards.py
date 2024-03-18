from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


# Клавиатура для стартового сообщения админам
def get_admin_practice_menu_kb():
    buttons = [[
            types.InlineKeyboardButton(text="Проверить участников", callback_data="CheckStudents")],
            [types.InlineKeyboardButton(text="Добавить предмет", callback_data="AddLesson"),
            types.InlineKeyboardButton(text="Удалить предмет", callback_data="DeleteLesson")],
            [types.InlineKeyboardButton(text="Добавить занятие", callback_data="AddPractice"),
            types.InlineKeyboardButton(text="Убрать занятие", callback_data="DeletePractice")],
            [types.InlineKeyboardButton(text="Посмотреть причины отказов", callback_data="CheckQuitReasons")],
            [types.InlineKeyboardButton(text="Вернуться в главное меню", callback_data="CancelAdminOperation")],
            [types.InlineKeyboardButton(text="Очистить занятия", callback_data="ClearPractices")]
        ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_admin_workshop_menu_kb():
    buttons = [[
            types.InlineKeyboardButton(text="Посмотреть участников", callback_data="CheckStudentsWorkshop")],
            [types.InlineKeyboardButton(text="Добавить мастерскую", callback_data="AddWorkshop"),
            types.InlineKeyboardButton(text="Удалить мастерскую", callback_data="DeleteWorkshop")],
            [types.InlineKeyboardButton(text="Добавить занятие в мастерской", callback_data="AddWorkshopPractice"),
            types.InlineKeyboardButton(text="Удалить занятие из мастерской", callback_data="DeleteWorkshopPractice")],
            [types.InlineKeyboardButton(text="Посмотреть отказы", callback_data="CheckQuitWorkshopReasons")],
            [types.InlineKeyboardButton(text="Вернуться в главное меню", callback_data="CancelAdminOperation")]
        ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_start_admin_menu_kb():
    buttons = [
            [types.InlineKeyboardButton(text="Практики", callback_data="AdminPractice")],
            [types.InlineKeyboardButton(text="Мастерские", callback_data="AdminWorkshop")],
            [types.InlineKeyboardButton(text="Отправить уведомление", callback_data="SendAdminToUsers")],
            [types.InlineKeyboardButton(text="Получить меню менторов", callback_data="CancelUserOperation")]
        ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


# Клавиатура для стартового сообщения пользователям
def get_start_user_kb():
    
    buttons = [[types.InlineKeyboardButton(
            text="🚀 Меню",
            callback_data="menu1")
    ]]
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

# Клавиатура для меню
def get_menu_kb():

    buttons = [
        [types.InlineKeyboardButton(text="🗺 Дорожная карта", callback_data="roadmap")],
        [types.InlineKeyboardButton(text="📚 Занятия", callback_data="SignOrQuitPractice")],
        [types.InlineKeyboardButton(text="⚙️ Мастерские", callback_data="Workshops")],
        [types.InlineKeyboardButton(text="📝 Оставить отзыв на занятие", callback_data="Feedback")],
        [types.InlineKeyboardButton(text="📣 Связаться с нами", callback_data="Connect")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

# Клавиатура для дорожной карты
def get_roadmap_kb():

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="🛣 Дорожная карта с описанием занятий", 
        url="https://miro.com/app/board/o9J_luc0BEE=/" )
    )
    builder.row(types.InlineKeyboardButton(
        text="🚀 Меню", callback_data="menu")
    )
    keyboard = builder.as_markup()
    
    return keyboard

# Универсальная клавиатура
def get_admin_number_list_kb(items: list[str]) -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item, callback_data=item)
    
    builder.row(types.InlineKeyboardButton(
        text="Отмена", callback_data="CancelAdminOperation")
    )
    if len(items) > 14:
        builder.adjust(7)
    elif len(items) > 9:
        builder.adjust(4)
    else:
        builder.adjust(3)

    return builder.as_markup()

def get_admin_list_kb(items: list[str]) -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item, callback_data=item)
    
    builder.row(types.InlineKeyboardButton(
        text="Отмена", callback_data="CancelAdminOperation")
    )
    
    return builder.as_markup()

def get_user_list_kb(items: list[str]) -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item, callback_data=item)
    
    builder.row(types.InlineKeyboardButton(
        text="📋 Меню", callback_data="CancelUserOperation")
    )
    builder.adjust(1)

    return builder.as_markup()

def get_user_list_cancel_sign_up(items: list[str]) -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item, callback_data=item)
    
    builder.row(types.InlineKeyboardButton(
        text="⬅️ Назад", callback_data="SignOrQuitPractice")
    )
    builder.row(types.InlineKeyboardButton(
        text="🚀 Меню", callback_data="CancelUserOperation")
    )
    builder.adjust(1)

    return builder.as_markup()

def get_user_list_cancel_workshop_sign_up(items: list[str]) -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item, callback_data=item)
    
    builder.row(types.InlineKeyboardButton(
        text="⬅️ Назад", callback_data="Workshops")
    )
    builder.row(types.InlineKeyboardButton(
        text="🚀 Меню", callback_data="CancelUserOperation")
    )
    builder.adjust(1)

    return builder.as_markup()


# Сохранение данных
def get_save_lesson_kb():
    
    buttons = [
        [types.InlineKeyboardButton(text="Сохранить", callback_data="save_lesson")],
        [types.InlineKeyboardButton(text="Отмена", callback_data="CancelAdminOperation")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_save_workshop_kb():
    
    buttons = [
        [types.InlineKeyboardButton(text="Сохранить", callback_data="save_workshop")],
        [types.InlineKeyboardButton(text="Отмена", callback_data="CancelAdminOperation")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

# Удаление данных
def delete_admin_practice_kb():

    buttons = [
        [types.InlineKeyboardButton(text="Подтвердить", callback_data="Accepting")],
        [types.InlineKeyboardButton(text="Отмена", callback_data="CancelAdminOperation")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_user_accept_kb():
    buttons = [
        [types.InlineKeyboardButton(text="✔️ Подтвердить", callback_data="AcceptingUser")],
        [types.InlineKeyboardButton(text="❌ Отмена", callback_data="CancelUserOperation")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard
# Кнопка возвращения в меню
def get_back_to_admin_menu_kb():

    buttons = [
        [types.InlineKeyboardButton(text="Меню", callback_data="CancelAdminOperation")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_back_to_user_menu_kb():

    buttons = [
        [types.InlineKeyboardButton(text="🚀 Меню", callback_data="CancelUserOperation")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_user_added_practice_kb():

    buttons = [
        [types.InlineKeyboardButton(text="✔️ Подтвердить", callback_data="Accepting")],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="CancelToChoosingDatetimeOperation")],
        [types.InlineKeyboardButton(text="🚀 Меню", callback_data="CancelUserOperation")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_user_added_workshop_practice_kb():

    buttons = [
        [types.InlineKeyboardButton(text="✔️ Подтвердить", callback_data="Accepting")],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="CancelToChoosingWorkshopDatetimeOperation")],
        [types.InlineKeyboardButton(text="🚀 Меню", callback_data="CancelUserOperation")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_user_registration_kb():

    buttons = [
        [types.InlineKeyboardButton(text="🌠 Вперёд!", callback_data="UserRegistration")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_user_finish_registration_kb():
    buttons = [
        [types.InlineKeyboardButton(text="✔️ Подтвердить", callback_data="AcceptUserRegistration"),
        types.InlineKeyboardButton(text="🔄 Ввести данные заново", callback_data="CancelUserRegistration")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


def get_user_sign_or_quit_practice_kb():
    buttons = [
        [types.InlineKeyboardButton(text="😊 Записаться", callback_data="SignUpForPractice"),
        types.InlineKeyboardButton(text="🤐 Отписаться", callback_data="QuitFromPractice")],
        [types.InlineKeyboardButton(text="📋 Мои занятия", callback_data="CheckForMyPractices")],
        [types.InlineKeyboardButton(text="🚀 Меню", callback_data="CancelUserOperation")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_3_points_kb():
    buttons = [
        [types.InlineKeyboardButton(text="1️⃣", callback_data="1"),
        types.InlineKeyboardButton(text="2️⃣", callback_data="2"),
        types.InlineKeyboardButton(text="3️⃣", callback_data="3")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_user_list_cancel_sign_up_practice_kb(items):
    
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item, callback_data=item)
    
    builder.row(types.InlineKeyboardButton(
        text="⬅️ Назад", callback_data="CancelToChoosingPracticeOperation")
    )
    builder.row(types.InlineKeyboardButton(
        text="🚀 Меню", callback_data="CancelUserOperation")
    )
    builder.adjust(1)

    return builder.as_markup()

def get_user_list_cancel_sign_up_workshop_practice_kb(items):
    
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item, callback_data=item)
    
    builder.row(types.InlineKeyboardButton(
        text="⬅️ Назад", callback_data="CancelToChoosingWorkshopPracticeOperation")
    )
    builder.row(types.InlineKeyboardButton(
        text="🚀 Меню", callback_data="CancelUserOperation")
    )
    builder.adjust(1)

    return builder.as_markup()

def get_user_list_cancel_sign_up_format_kb(items):
    
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item, callback_data=item)
    
    builder.row(types.InlineKeyboardButton(
        text="⬅️ Назад", callback_data="CancelToChoosingFormatOperation")
    )
    builder.row(types.InlineKeyboardButton(
        text="🚀 Меню", callback_data="CancelUserOperation")
    )
    builder.adjust(1)

    return builder.as_markup()

def get_user_list_cancel_sign_up_workshop_format_kb(items):
    
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item, callback_data=item)
    
    builder.row(types.InlineKeyboardButton(
        text="⬅️ Назад", callback_data="CancelToChoosingWorkshopFormatOperation")
    )
    builder.row(types.InlineKeyboardButton(
        text="🚀 Меню", callback_data="CancelUserOperation")
    )
    builder.adjust(1)

    return builder.as_markup()

def get_user_accepting_quit_kb():
    buttons = [
        [types.InlineKeyboardButton(text="✔️ Подтвердить", callback_data="Accepting")],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="CancelToChoosingReasonForQuitOperation")],
        [types.InlineKeyboardButton(text="🚀 Меню", callback_data="CancelUserOperation")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_user_cancel_quit_practice_kb(items):
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item, callback_data=item)
    
    builder.row(types.InlineKeyboardButton(
        text="⬅️ Назад", callback_data="CancelToChoosingPracticeForQuitOperation")
    )
    builder.row(types.InlineKeyboardButton(
        text="🚀 Меню", callback_data="CancelUserOperation")
    )
    builder.adjust(1)

    return builder.as_markup()

def get_user_cancel_quit_reason_kb(items):
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item, callback_data=item)
    
    builder.row(types.InlineKeyboardButton(
        text="⬅️ Назад", callback_data="CancelToChoosingReasonForQuitOperation")
    )
    builder.row(types.InlineKeyboardButton(
        text="🚀 Меню", callback_data="CancelUserOperation")
    )
    builder.adjust(1)

    return builder.as_markup()

def get_user_cancel_quit_kb(items):
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item, callback_data=item)
    
    builder.row(types.InlineKeyboardButton(
        text="⬅️ Назад", callback_data="SignOrQuitPractice")
    )
    builder.row(types.InlineKeyboardButton(
        text="🚀 Меню", callback_data="CancelUserOperation")
    )
    builder.adjust(1)

    return builder.as_markup()

def get_user_workshop_menu_kb():
    buttons = [
        [types.InlineKeyboardButton(text="📑 Описание мастерских", callback_data="WorkshopDescriptions")],
        [types.InlineKeyboardButton(text="😊 Записаться", callback_data="SignUpForWorkshopPractice"),
        types.InlineKeyboardButton(text="🤐 Отписаться", callback_data="QuitWorkshop")],
        [types.InlineKeyboardButton(text="📋 Мои записи", callback_data="CheckOwnWorkshop")],
        [types.InlineKeyboardButton(text="🚀 Меню", callback_data="CancelUserOperation")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_back_to_user_own_practices_menu_kb():
    buttons = [
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="CheckForMyPractices")],
        [types.InlineKeyboardButton(text="🚀 Меню", callback_data="CancelUserOperation")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_back_to_user_practice_menu_kb(items):
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item, callback_data=item)
    
    builder.row(types.InlineKeyboardButton(
        text="⬅️ Назад", callback_data="SignOrQuitPractice")
    )
    builder.row(types.InlineKeyboardButton(
        text="🚀 Меню", callback_data="CancelUserOperation")
    )
    builder.adjust(1)

    return builder.as_markup()

def get_back_to_user_own_workshop_menu_kb():

    buttons = [
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="CheckOwnWorkshop")],
        [types.InlineKeyboardButton(text="🚀 Меню", callback_data="CancelUserOperation")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_back_to_user_workshop_menu_kb(items):

    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item, callback_data=item)
    
    builder.row(types.InlineKeyboardButton(
        text="⬅️ Назад", callback_data="Workshops")
    )
    builder.row(types.InlineKeyboardButton(
        text="🚀 Меню", callback_data="CancelUserOperation")
    )
    builder.adjust(1)

    return builder.as_markup()
