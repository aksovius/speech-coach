import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from server.bot.keyboards.menu_keyboards import (
    MODE_ARCHITECTURE,
    get_architecture_start_keyboard,
)
from shared.services.question_manager import set_user_question
from shared.services.question_service import get_question_for_user

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == MODE_ARCHITECTURE)
async def handle_architecture_mode(callback_query: CallbackQuery):
    logger.info(f"Architecture mode selected by user {callback_query.from_user.id}")
    try:
        await callback_query.answer("Architecture mode selected")
        await callback_query.message.edit_text(
            "You will be asked a question about software architecture.\n"
            "You will have time to prepare and answer. Note that answers longer than 3 minutes will be truncated.\n"
            "Are you ready to begin?",
            reply_markup=get_architecture_start_keyboard(),
        )
    except TelegramBadRequest as e:
        if "query is too old" in str(e):
            logger.warning(
                f"Callback query is too old for user {callback_query.from_user.id}"
            )
            return
        raise


@router.callback_query(F.data == "mode_architecture_start")
async def handle_architecture_start(
    callback_query: CallbackQuery, db: AsyncSession, user_id: int
):
    try:
        logger.info(
            f"Starting architecture questions for user {callback_query.from_user.id}"
        )
        await callback_query.answer("Starting")
        question = await get_question_for_user(user_id, db, "architecture")
        if not question:
            logger.error(f"No question found for user {user_id}")
            await callback_query.message.answer("❌ Error: No questions available")
            return

        question.question_category = "architecture"
        set_user_question(callback_query.from_user.id, question)

        # Remove reply buttons
        await callback_query.message.edit_reply_markup(reply_markup=None)

        await callback_query.message.answer(
            f"<b>Question:</b>\n{question.text}", parse_mode="HTML"
        )
    except TelegramBadRequest as e:
        if "query is too old" in str(e):
            logger.warning(
                f"Callback query is too old for user {callback_query.from_user.id}"
            )
            return
        raise
    except Exception as e:
        logger.error(f"Error in handle_architecture_start: {str(e)}", exc_info=True)
        await callback_query.message.answer(
            "❌ An error occurred while processing your request"
        )
