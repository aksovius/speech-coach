import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery

from server.bot.keyboards.menu_keyboards import get_toefl_keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "mode_toefl")
async def handle_toefl_mode(callback_query: CallbackQuery):
    logger.info(f"TOEFL mode selected by user {callback_query.from_user.id}")
    await callback_query.answer("TOEFL mode selected")
    await callback_query.message.edit_text(
        "Select TOEFL speaking task:", reply_markup=get_toefl_keyboard()
    )


@router.callback_query(F.data.startswith("mode_toefl_speaking"))
async def handle_toefl_speaking(callback_query: CallbackQuery):
    speaking_task = callback_query.data.replace("mode_toefl_speaking", "")
    logger.info(
        f"TOEFL Speaking {speaking_task} selected by user {callback_query.from_user.id}"
    )

    await callback_query.answer(f"TOEFL Speaking {speaking_task} selected")
    await callback_query.message.edit_text(
        f"You selected TOEFL Speaking {speaking_task}. Let's begin!", reply_markup=None
    )
