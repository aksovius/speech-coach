from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Bot modes
MODE_TOEFL = "mode_toefl"
MODE_INTERVIEW = "mode_interview"
MODE_ALGORITHMS = "mode_algorithms"
MODE_BACK = "mode_back"

# TOEFL speaking tasks
MODE_TOEFL_SPEAKING1 = "mode_toefl_speaking1"
MODE_TOEFL_SPEAKING2 = "mode_toefl_speaking2"
MODE_TOEFL_SPEAKING3 = "mode_toefl_speaking3"
MODE_TOEFL_SPEAKING4 = "mode_toefl_speaking4"
MODE_TOEFL_START = "mode_toefl_start_{task}"


def get_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="TOEFL", callback_data=MODE_TOEFL)],
            [InlineKeyboardButton(text="Interview", callback_data=MODE_INTERVIEW)],
            [InlineKeyboardButton(text="Algorithms", callback_data=MODE_ALGORITHMS)],
        ]
    )
    return keyboard


def get_toefl_keyboard() -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="SPEAKING 1", callback_data=MODE_TOEFL_SPEAKING1
                ),
                InlineKeyboardButton(
                    text="SPEAKING 2", callback_data=MODE_TOEFL_SPEAKING2
                ),
            ],
            [
                InlineKeyboardButton(
                    text="SPEAKING 3", callback_data=MODE_TOEFL_SPEAKING3
                ),
                InlineKeyboardButton(
                    text="SPEAKING 4", callback_data=MODE_TOEFL_SPEAKING4
                ),
            ],
            [InlineKeyboardButton(text="« Back", callback_data=MODE_BACK)],
        ]
    )
    return keyboard


def get_toefl_start_keyboard(task_number: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="« Back", callback_data=MODE_TOEFL),
                InlineKeyboardButton(
                    text="Start",
                    callback_data=MODE_TOEFL_START.format(task=task_number),
                ),
            ],
        ]
    )
    return keyboard
