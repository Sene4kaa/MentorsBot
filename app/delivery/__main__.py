import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from django.conf import settings

from bot.handlers import exit, common
from bot.handlers.admin_panel import admin_practice_menu, admin_workshop_menu, admin_send_to_users
from bot.handlers.admin_panel.practices import (
    admin_add_practice,
    admin_delete_lesson,
    admin_delete_practice,
    admin_new_lesson,
    admin_check_students,
    admin_quited_practice_reasons,
    admin_check_practice
)
from bot.handlers.admin_panel.workshops import (
    admin_add_workshop,
    admin_add_workshop_practice,
    admin_delete_workshop,
    admin_delete_workshop_practice,
    admin_check_students_wokrshop,
    admin_quited_workshops_reasons,
)


async def main():
    from bot.handlers.user_panel import user_menu, roadmap, user_registration, user_feedback, user_send_message
    from bot.handlers.user_panel.practices import (
        sign_or_quit_practice,
        sign_up_for_practice,
        user_check_own_practices,
        user_quit_from_practice,
    )
    from bot.handlers.user_panel.workshops import (
        user_workshop_menu,
        sign_up_for_workshop,
        user_check_own_workshop,
        user_quit_from_workshop,
        user_workshop_description,
    )

    logging.basicConfig(level=logging.INFO)
    bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    dp.include_routers(
        common.router,
        admin_practice_menu.router,
        admin_workshop_menu.router,
        admin_send_to_users.router,
        admin_add_practice.router,
        admin_delete_lesson.router,
        admin_delete_practice.router,
        admin_new_lesson.router,
        admin_check_students.router,
        admin_quited_practice_reasons.router,
        admin_check_practice.router,
        admin_add_workshop.router,
        admin_add_workshop_practice.router,
        admin_delete_workshop.router,
        admin_delete_workshop_practice.router,
        admin_check_students_wokrshop.router,
        admin_quited_workshops_reasons.router,
        user_menu.router,
        roadmap.router,
        user_registration.router,
        user_feedback.router,
        user_send_message.router,
        sign_or_quit_practice.router,
        sign_up_for_practice.router,
        user_check_own_practices.router,
        user_quit_from_practice.router,
        user_workshop_menu.router,
        sign_up_for_workshop.router,
        user_check_own_workshop.router,
        user_quit_from_workshop.router,
        user_workshop_description.router,
        exit.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    current_path = Path(__file__).resolve().parent.parent
    with open(current_path / "test.json", "w") as credentials_file:
        credentials_file.write(settings.GSPREAD)

    asyncio.run(main())
