import logging
import os
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PicklePersistence,
    filters,
)

from agenssistant_agent.agent import agentssistant
from agenssistant_bot.utils import helpers, initializer
from agenssistant_bot.workflows import google_calendar_setup

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class Initializer(initializer.Initializer):
    def is_initialized(self, context: ContextTypes.DEFAULT_TYPE) -> bool:
        return "is_initialized" in context.user_data

    def __call__(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        context.user_data["agent_chat"] = []
        context.user_data["is_initialized"] = True


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


@initializer.EnsureInitialized(initializer=Initializer())
async def agent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Interact with the agent."""

    context.user_data["agent_chat"].append({"role": "user", "content": update.message.text, "timestamp": time.time()})
    conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in context.user_data["agent_chat"]])

    result = await agentssistant.run(conversation, deps=helpers.build_agent_deps(update, context))

    context.user_data["agent_chat"].append({"role": "assistant", "content": result.data, "timestamp": time.time()})

    await update.message.reply_text(result.data)


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
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, agent))

    # Run poll
    application.run_polling()


if __name__ == "__main__":
    main()
