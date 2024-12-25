import importlib
from MainBot import (
    LOGGER,
    application,
    ERROR_LOGS,
    LOGGER,
    BOT_USERNAME,
    DEV_USERNAME,
    FIRST_NAMES,
    CURRENT_USERS,
    ADMINS,
    VALID_CHAT_IDS,
    JOB_QUEUE,
)
import traceback
import json
from MainBot.modules import ALL_MODULES
from telegram import Update
import html
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode
import MainBot.modules.mongo.users as users
import MainBot.modules.mongo.extra_stuff as extra_stuff
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from MainBot.modules.helper_funcs.helper import reply_to_message
from MainBot.modules.users import log_user
import datetime
import pytz
import io

IMPORTED = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("MainBot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")


async def load_user_first_names():
    global FIRST_NAMES
    CURR_USER_FIRST_NAMES = await users.get_all_users()
    for el in CURR_USER_FIRST_NAMES:
        FIRST_NAMES[el] = CURR_USER_FIRST_NAMES[el]["first_name"]


async def load_all_users():
    global CURRENT_USERS
    all_users = await users.get_all_users()
    for el in all_users:
        CURRENT_USERS.add(el)


async def load_all_admins():
    global ADMINS
    all_admins = await extra_stuff.get_all_higher_users()
    for el in all_admins:
        ADMINS.add(el)


async def load_all_valid_chats():
    global VALID_CHAT_IDS
    all_chats = await extra_stuff.get_all_valid_chats()
    for el in all_chats:
        VALID_CHAT_IDS.add(el)


async def load_all_data(context: ContextTypes.DEFAULT_TYPE):
    await load_user_first_names()
    await load_all_valid_chats()
    await load_all_admins()
    await load_all_users()


def start_all_data_load_job():
    JOB_QUEUE.run_once(
        load_all_data,
        1,
        name="load_all_data",
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await log_user(user)
    first_name = user.first_name
    message = update.effective_message
    msg = ""
    msg = f"Hey there *{first_name}*!\nThis is @{BOT_USERNAME}\n\nA telegram bot which can help you accept users join request automatically.\n\nMade with ❤️ By @{DEV_USERNAME}"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Add To Channel",
                    url=f"https://t.me/{BOT_USERNAME}?startchannel",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Add To Group",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup",
                ),
            ],
        ]
    )
    await reply_to_message(
        message,
        msg,
        context.bot,
        update.effective_chat.id,
        ParseMode.MARKDOWN,
        keyboard,
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    if "RemoteDisconnected" in context.error.__format__(""):
        return
    LOGGER.error("Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    n = len(message)
    if n > 2000:
        message = (
            "An exception was raised while handling an update\n"
            f"update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}\n\n"
            f"context.chat_data = {html.escape(str(context.chat_data))}\n\n"
            f"context.user_data = {html.escape(str(context.user_data))}\n\n"
            f"{html.escape(tb_string)}"
        )
        with io.BytesIO(str.encode(message)) as out_file:
            out_file.name = "error logs.txt"
            await context.bot.send_document(chat_id=ERROR_LOGS, document=out_file)
    else:
        await context.bot.send_message(
            chat_id=ERROR_LOGS, text=message, parse_mode=ParseMode.HTML
        )


def main() -> None:
    application.add_handler(CommandHandler("start", start))
    application.add_error_handler(error_handler)
    start_all_data_load_job()
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))

    main()
