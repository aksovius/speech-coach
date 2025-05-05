from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

from shared.config import settings

router = Router()


@router.message(Command("statistics"))
async def handle_question(message: Message, **kwargs):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Open Statistics",
                    web_app=WebAppInfo(url=settings.STATISTICS_API_URL),
                )
            ]
        ]
    )
    await message.answer(
        "Click the button below to open statistics:", reply_markup=keyboard
    )
