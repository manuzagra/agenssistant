from telegram import Update


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
