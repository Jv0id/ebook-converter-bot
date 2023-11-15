"""Bot main module."""

from telethon import events

from ebook_converter_bot.bot import BOT, BOT_INFO
from ebook_converter_bot.db.curd import add_chat_to_db, get_lang
from ebook_converter_bot.utils.i18n import translate as _
from ebook_converter_bot.utils.telegram import (
    get_chat_name,
    get_chat_type,
    tg_exceptions_handler,
)


@BOT.on(events.NewMessage(pattern="/start"))
@tg_exceptions_handler
async def start(event: events.NewMessage.Event) -> None:
    """Send a message when the command /start is sent."""
    add_chat_to_db(event.chat_id, get_chat_name(event), get_chat_type(event))
    await event.reply(
        _(
            "Hello {}!\n\n \
        This bot allows you to convert E-Books to various formats.\n\n \
        The bot is open source, you can find the source code of it [here](https://github.com/Jv0id/ebook-converter-bot).\n \
        Maintained by: [jp0id](https://t.me/pm_jp_bot/).",
            get_lang(event.chat_id),
        ).format(
            event.chat.first_name
            if hasattr(event.chat, "first_name")
            else event.chat.title
        )
    )


# Add new chats to database
@BOT.on(
    events.chataction.ChatAction(
        func=lambda event: event.user_added and BOT_INFO["id"] == event.user_id
    )
)
async def on_adding_to_chat(event: events.NewMessage.Event) -> None:
    """Adds the chat that bot was added to into the database."""
    add_chat_to_db(event.chat_id, get_chat_name(event), get_chat_type(event))
