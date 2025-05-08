import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from server.bot.keyboards.menu_keyboards import (
    MODE_TOEFL,
    MODE_TOEFL_SPEAKING1,
    MODE_TOEFL_SPEAKING2,
    MODE_TOEFL_SPEAKING3,
    MODE_TOEFL_SPEAKING4,
    get_toefl_keyboard,
    get_toefl_start_keyboard,
)
from shared.services.question_manager import set_user_question
from shared.services.question_service import get_question_for_user

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == MODE_TOEFL)
async def handle_toefl_mode(callback_query: CallbackQuery):
    logger.info(f"TOEFL mode selected by user {callback_query.from_user.id}")
    try:
        await callback_query.answer("TOEFL mode selected")
        await callback_query.message.edit_text(
            "Select TOEFL speaking task:", reply_markup=get_toefl_keyboard()
        )
    except TelegramBadRequest as e:
        if "query is too old" in str(e):
            logger.warning(
                f"Callback query is too old for user {callback_query.from_user.id}"
            )
            return
        raise


@router.callback_query(
    F.data.in_(
        [
            MODE_TOEFL_SPEAKING1,
            MODE_TOEFL_SPEAKING2,
            MODE_TOEFL_SPEAKING3,
            MODE_TOEFL_SPEAKING4,
        ]
    )
)
async def handle_toefl_speaking(callback_query: CallbackQuery):
    speaking_task = callback_query.data.replace("mode_toefl_speaking", "")
    logger.info(
        f"TOEFL speaking task {speaking_task} selected by user {callback_query.from_user.id}"
    )
    try:
        await callback_query.answer(f"TOEFL speaking task {speaking_task} selected")
        task_description = {
            MODE_TOEFL_SPEAKING1: "TOEFL Speaking Task 1: Independent Speaking",
            MODE_TOEFL_SPEAKING2: "TOEFL Speaking Task 2: Independent Speaking",
            MODE_TOEFL_SPEAKING3: "TOEFL Speaking Task 3: Integrated Speaking",
            MODE_TOEFL_SPEAKING4: "TOEFL Speaking Task 4: Integrated Speaking",
        }.get(callback_query.data, "TOEFL Speaking Task")

        await callback_query.message.edit_text(
            f"{task_description}\n\n"
            "You will be asked to speak about a familiar topic. "
            "You will have 15 seconds to prepare and 45 seconds to speak.\n\n"
            "Are you ready to begin?",
            reply_markup=get_toefl_start_keyboard(speaking_task),
        )
    except TelegramBadRequest as e:
        if "query is too old" in str(e):
            logger.warning(
                f"Callback query is too old for user {callback_query.from_user.id}"
            )
            return
        raise


@router.callback_query(F.data.startswith("mode_toefl_start_"))
async def handle_toefl_start(
    callback_query: CallbackQuery, db: AsyncSession, user_id: int
):
    try:
        task_number = callback_query.data.split("_")[-1]
        logger.info(
            f"Starting TOEFL speaking task {task_number} for user {callback_query.from_user.id}"
        )
        await callback_query.answer(f"Starting TOEFL speaking task {task_number}")
        category = f"toefl{task_number}"
        question = await get_question_for_user(user_id, db, category)
        if not question:
            logger.error(f"No question found for user {user_id}")
            await callback_query.message.answer("❌ Error: No question available")
            return

        set_user_question(callback_query.from_user.id, question)

        # Delete the reply buttons
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
        logger.error(f"Error in handle_toefl_start: {str(e)}", exc_info=True)
        await callback_query.message.answer(
            "❌ An error occurred while processing your request"
        )
