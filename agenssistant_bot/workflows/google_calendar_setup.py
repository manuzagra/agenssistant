import logging

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from agenssistant_bot.utils import google_auth, helpers

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# google calendar scope
SCOPES = ["https://www.googleapis.com/auth/calendar"]


# standarize things
CALLBACK_DATA = "google_calendar_setup"
DESCRIPTION = "Setup Google Calendar"


# States
_INSTRUCTIONS, _TOKEN, _ERROR = range(3)


# Conversation Handlers
async def _display_instructions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display instructions to set up the Google Calendar API and provide the link to authorize the bot."""

    if google_auth.get_google_credentials(context, SCOPES, refresh=True):
        text = "Google Calendar is already set up."
        await helpers.reply_text_everywhere(update, text)
        return ConversationHandler.END

    flow = google_auth.get_google_auth_flow(SCOPES)
    if flow is None:
        return _ERROR

    auth_url, state = flow.authorization_url(access_type="offline", prompt="consent")
    context.user_data["google_auth_flow_state"] = state

    text = """
           To be able to access your google calendar first you need to grant access to the bot.
           To do this you need to follow the link the bot will provide, grant access and get the token.
           Then you need to give that token to the bot.\n
           """
    text += f"Please visit this URL to authorize:\n{auth_url}\n"
    text += "Then enter the authorization token:"

    await helpers.reply_text_everywhere(update, text)

    return _TOKEN


async def _process_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process the token provided by the user and store the credentials in the user context."""

    token = update.message.text.strip()

    flow = google_auth.get_google_auth_flow()

    flow.fetch_token(code=token, state=context.user_data["google_auth_flow_state"])
    context.user_data["google_auth_credentials_json"] = flow.credentials.to_json()

    await update.message.reply_text(
        "Authorization completed successfully. You can now use the bot with your Google Calendar."
    )

    return ConversationHandler.END


async def _error_notification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Notify the user that an error occurred while setting up the Google Calendar."""

    logger.error("It wasnt possible to finish the process of seting up the google calendar.")

    text = "There was an error while trying to set up the Google Calendar. The bot may not be correctly configured.\nPlease try again later."

    await helpers.reply_text_everywhere(update, text)

    return ConversationHandler.END


# conversation
conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler(CALLBACK_DATA, _display_instructions),
        CallbackQueryHandler(_display_instructions, pattern=f"^{CALLBACK_DATA}$"),
    ],
    states={
        _INSTRUCTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, _display_instructions)],
        _TOKEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, _process_token)],
        _ERROR: [MessageHandler(filters.TEXT & ~filters.COMMAND, _error_notification)],
    },
    fallbacks=[MessageHandler(filters.TEXT & ~filters.COMMAND, _error_notification)],
)
