from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="TOEFL", callback_data="mode_toefl")],
            [InlineKeyboardButton(text="Interview", callback_data="mode_interview")],
            [InlineKeyboardButton(text="Algorithms", callback_data="mode_algorithms")],
        ]
    )
    return keyboard


def get_toefl_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="SPEAKING 1", callback_data="mode_toefl_speaking1"
                ),
                InlineKeyboardButton(
                    text="SPEAKING 2", callback_data="mode_toefl_speaking2"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="SPEAKING 3", callback_data="mode_toefl_speaking3"
                ),
                InlineKeyboardButton(
                    text="SPEAKING 4", callback_data="mode_toefl_speaking4"
                ),
            ],
            [InlineKeyboardButton(text="« Back", callback_data="mode_back")],
        ]
    )
    return keyboard
