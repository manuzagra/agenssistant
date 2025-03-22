from telegram import Update
from telegram.ext import ContextTypes

from agenssistant_common import types


async def reply_text_everywhere(
    update: Update, text: str, message: bool = True, channel_post: bool = True, callback_query: bool = True
) -> None:
    """Reply to the user, channel post, or callback query with the given text.

    Args:
        update (Update): The update object from `telegram.ext` used to send the response.
        text (str): Text to be send as a response.
        message (bool, optional): Answer a message if available. Defaults to True.
        channel_post (bool, optional): Answer a channel_post if available. Defaults to True.
        callback_query (bool, optional): Answer a callback_query if available. Defaults to True.
    """

    if message and update.message:
        await update.message.reply_text(text)
    if channel_post and update.channel_post:
        await update.channel_post.reply_text(text)
    if callback_query and update.callback_query:
        await update.callback_query.message.reply_text(text)


def build_agent_deps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> types.AgentDependencies:
    """ Helper to construct the dependencies for the agent.

    Args:
        update (Update): The update object from `telegram.ext`.
        context (ContextTypes.DEFAULT_TYPE): The context object from the telegram bot.

    Returns:
        types.AgentDependencies: The agent dependencies with the needed information.
    """
    
    msg = update.message if update.message else update.callback_query.message
    user = msg.from_user
    return types.AgentDependencies(
        user=types.TelegramUser(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            language_code=user.language_code,
        )
    )
