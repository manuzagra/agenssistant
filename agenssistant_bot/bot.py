import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    PicklePersistence,
)

from agenssistant_bot.workflows import google_calendar_setup

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""

    keyboard = [
        [
            InlineKeyboardButton(
                google_calendar_setup.DESCRIPTION,
                callback_data=google_calendar_setup.CALLBACK_DATA,
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Welcome! Choose an option:"
    await update.message.reply_text(text, reply_markup=reply_markup)


def main() -> None:
    # Get some environ variables
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    persistence_file = os.path.join(os.environ["DATA_PATH"], os.environ["PERSISTENCE_FILE"])

    # setup persistence
    persistence = PicklePersistence(filepath=persistence_file)

    # Create the Application
    application = Application.builder().token(token).persistence(persistence).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(google_calendar_setup.conversation_handler)

    # Run poll
    application.run_polling()


if __name__ == "__main__":
    main()
