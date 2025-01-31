import MainBot.modules.mongo.extra_stuff as extra_stuff
from telegram import Update
from MainBot import (
    application,
    ADMINS,
    FIRST_NAMES,
    CURRENT_USERS,
    VALID_CHAT_IDS,
)
from telegram.ext import ContextTypes
import html
from telegram.ext import CommandHandler
from telegram.constants import ParseMode
from telegram.helpers import mention_html
from MainBot.modules.helper_funcs.chat_status import admin_command, owner_command
from MainBot.modules.helper_funcs.helper import send_message_to_chat, reply_to_message


@owner_command
async def promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ADMINS
    message = update.message
    args = context.args
    to_user = message.reply_to_message
    msg, Flag = "", False
    if to_user:
        user_to_promote = str(to_user.from_user.id)
    elif len(args) > 0:
        user_to_promote = args[0]
    else:
        user_to_promote = ""
        msg = "Please give some id as well!"
        Flag = True
    if user_to_promote in ADMINS:
        msg = "This member is already a admin"
        Flag = True
    if Flag:
        await reply_to_message(message, msg, context.bot, update.effective_chat.id)
        return
    await extra_stuff.add_admin(user_to_promote)
    ADMINS.add(user_to_promote)
    await reply_to_message(
        message,
        f"\nSuccessfully promoted {user_to_promote}!",
        context.bot,
        update.effective_chat.id,
    )
    await send_message_to_chat(
        "You have been promoted to admin by Owner.", context.bot, user_to_promote
    )


@owner_command
async def admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ADMINS
    message = update.message
    msg = "<u>Admin List</u>\n\n"
    count = 1
    for el in ADMINS:
        msg += "{}) {} [{}]\n\n".format(
            count, mention_html(int(el), html.escape(FIRST_NAMES.get(el, "None"))), el
        )
    await reply_to_message(
        message,
        msg,
        context.bot,
        update.effective_chat.id,
    )


@owner_command
async def demote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ADMINS
    user_id = str(update.message.from_user.id)
    message = update.message
    args = context.args
    to_user = message.reply_to_message
    msg, Flag = "", False
    if to_user:
        user_to_demote = str(to_user.from_user.id)
    elif len(args) > 0:
        user_to_demote = args[0]
    else:
        user_to_demote = ""
        msg = "Please give some id as well!"
        Flag = True
    if user_to_demote not in ADMINS:
        msg = "This member is not an authorized member"
        Flag = True
    if user_to_demote == user_id:
        msg = "You can't demote yourself BAKA!"
        Flag = True
    if Flag:
        await reply_to_message(message, msg, context.bot, update.effective_chat.id)
        return

    if user_to_demote in ADMINS:
        ADMINS.remove(user_to_demote)
        await extra_stuff.remove_admin(user_to_demote)
    await reply_to_message(
        message,
        "\nSuccessfully demoted {}!".format(user_to_demote),
        context.bot,
        update.effective_chat.id,
    )
    await send_message_to_chat(
        "You have been demoted by Owner.", context.bot, user_to_demote
    )


@owner_command
async def remove_valid_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global VALID_CHAT_IDS
    message = update.message
    args = context.args
    msg, Flag = "", False
    if len(args) > 0:
        chat_to_validate = args[0]
    else:
        chat_to_validate = ""
        msg = "Please provide some chat id also."
        Flag = True
    if chat_to_validate not in VALID_CHAT_IDS:
        msg = "Chat is not part of allowed chats."
        Flag = True
    if Flag:
        await reply_to_message(message, msg, context.bot, update.effective_chat.id)
        return
    await extra_stuff.remove_valid_chat(chat_to_validate)
    VALID_CHAT_IDS.remove(chat_to_validate)
    await reply_to_message(
        message,
        "\nSuccessfully removed chat : {}".format(chat_to_validate),
        context.bot,
        update.effective_chat.id,
    )


@owner_command
async def add_valid_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global VALID_CHAT_IDS
    message = update.message
    args = context.args
    msg, Flag = "", False
    if len(args) > 0:
        chat_to_validate = args[0]
    else:
        chat_to_validate = ""
        msg = "Please provide some chat id also."
        Flag = True
    if chat_to_validate in VALID_CHAT_IDS:
        msg = "Chat is already added."
        Flag = True
    if Flag:
        await reply_to_message(message, msg, context.bot, update.effective_chat.id)
        return

    valid = await extra_stuff.add_valid_chat(chat_to_validate)
    if valid:
        VALID_CHAT_IDS.add(chat_to_validate)

        await reply_to_message(
            message,
            "\nSuccessfully added chat : {}".format(chat_to_validate),
            context.bot,
            update.effective_chat.id,
        )
    else:
        await reply_to_message(
            message,
            "\nUnable to add chat : {}".format(chat_to_validate),
            context.bot,
            update.effective_chat.id,
        )


def handle_slash(message):
    if "``" in message:
        arr = list(message.split("``"))
        i = 0
        ret = ""
        for el in arr:
            if i % 2 == 0:
                ret += el
            else:
                ret += "`" + el + "`"
            i += 1
        return ret
    else:
        return message


@admin_command
async def userss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CURRENT_USERS
    message = update.message
    msg = "<b>Total Users : {}</b>".format(len(CURRENT_USERS))
    await reply_to_message(
        message, msg, context.bot, update.effective_chat.id, ParseMode.HTML
    )


USERS_HANDLER = CommandHandler("users", userss)
PROMOTE_HANDLER = CommandHandler(["promote", "addadmins"], promote)
DEMOTE_HANDLER = CommandHandler(["demote", "removeadmins"], demote)
ADMIN_LIST_HANDLER = CommandHandler(["adminlist", "admins"], admins)
ADD_VALID_CHAT_HANDLER = CommandHandler("add", add_valid_chat)
REMOVE_VALID_CHAT_HANDLER = CommandHandler("remove", remove_valid_chat)
application.add_handler(USERS_HANDLER)
application.add_handler(PROMOTE_HANDLER)
application.add_handler(DEMOTE_HANDLER)
application.add_handler(ADMIN_LIST_HANDLER)
application.add_handler(ADD_VALID_CHAT_HANDLER)
application.add_handler(REMOVE_VALID_CHAT_HANDLER)

__mod_name__ = "Owner"
__handlers__ = [
    USERS_HANDLER,
    DEMOTE_HANDLER,
    PROMOTE_HANDLER,
    ADMIN_LIST_HANDLER,
    ADD_VALID_CHAT_HANDLER,
    REMOVE_VALID_CHAT_HANDLER,
]
