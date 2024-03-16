from aiogram import Router, F
from aiogram.types import Message


router = Router()

@router.message(F.text)
async def deleting_message(message: Message):

    await message.delete()