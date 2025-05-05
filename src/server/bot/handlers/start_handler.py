import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from server.bot.keyboards.menu_keyboards import get_main_keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("start"))
async def handle_start(message: Message):
    logger.info(f"Start command received from user {message.from_user.id}")
    await message.answer("Select a mode:", reply_markup=get_main_keyboard())


@router.callback_query(F.data == "mode_back")
async def handle_back(callback_query: CallbackQuery):
    logger.info(f"Back button pressed by user {callback_query.from_user.id}")
    await callback_query.answer("Returning to main menu")
    await callback_query.message.edit_text(
        "Select a mode:", reply_markup=get_main_keyboard()
    )


@router.callback_query(F.data.in_(["mode_interview", "mode_algorithms"]))
async def handle_other_modes(callback_query: CallbackQuery):
    mode = callback_query.data.replace("mode_", "")
    logger.info(f"{mode.title()} mode selected by user {callback_query.from_user.id}")

    await callback_query.answer(f"{mode.title()} mode selected")
    await callback_query.message.edit_text(
        f"You selected {mode.title()} mode. Let's begin!", reply_markup=None
    )
