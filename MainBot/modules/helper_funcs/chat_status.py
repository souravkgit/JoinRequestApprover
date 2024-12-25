from functools import wraps
from MainBot import (
    ADMINS,
    OWNER_ID,
    CURRENT_USERS,
    BOT_USERNAME,
)
from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from MainBot.modules.helper_funcs.helper import reply_to_message

from telegram.constants import ParseMode


def owner_command(func):
    @wraps(func)
    async def is_owner(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        user = update.effective_user
        query = update.callback_query
        user_id = str(user.id)
        if query:
            user_id = str(query.from_user.id)
            if user_id not in CURRENT_USERS:
                await query.answer("You can't use this.")
            else:
                await func(update, context, *args, **kwargs)
            return
        message = update.effective_message
        if user_id == OWNER_ID:
            return await func(update, context, *args, **kwargs)
        else:
            await reply_to_message(
                message,
                "You are not allowed to use this.",
                context.bot,
                update.effective_chat.id,
            )

    return is_owner


def group_command(func):
    @wraps(func)
    async def is_command_used_in_group(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        query = update.callback_query
        if query:
            chat = query.message.chat
            if chat.type == "private":
                await query.answer("Please use this in groups only.")
            else:
                await func(update, context, *args, **kwargs)
            return
        chat = update.effective_chat
        message = update.effective_message
        if chat.type == "private":
            return await reply_to_message(
                message,
                "Please use the command in groups only.",
                context.bot,
                update.effective_chat.id,
            )
        else:
            return await func(update, context, *args, **kwargs)

    return is_command_used_in_group


def admin_command(func):
    @wraps(func)
    async def is_owner(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        user = update.effective_user
        query = update.callback_query
        user_id = str(user.id)
        if query:
            user_id = str(query.from_user.id)
            if user_id not in ADMINS:
                await query.answer("You can't use this.")
            else:
                await func(update, context, *args, **kwargs)
            return
        message = update.effective_message
        if user_id in ADMINS:
            return await func(update, context, *args, **kwargs)
        else:
            await reply_to_message(
                message,
                "You are not allowed to use this.",
                context.bot,
                update.effective_chat.id,
            )

    return is_owner


def registered(func):
    @wraps(func)
    async def is_registered(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        user = update.effective_user
        query = update.callback_query
        user_id = str(user.id)
        if query:
            if user_id not in CURRENT_USERS:
                await query.answer("You need to register first")
            else:
                await func(update, context, *args, **kwargs)
            return
        message = update.effective_message
        if user_id in CURRENT_USERS:
            return await func(update, context, *args, **kwargs)
        else:
            await reply_to_message(
                message,
                "You need to register first, please start the bot.",
                context.bot,
                update.effective_chat.id,
                ParseMode.MARKDOWN,
                InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Start Bot",
                                url=f"https://t.me/{BOT_USERNAME}",
                            )
                        ]
                    ]
                ),
            )

    return is_registered


async def is_user_in_chat(bot, chat, user_id):
    try:
        member = await bot.get_chat_member(chat, user_id)
        if member:
            return member.status not in ("left", "kicked", "banned")
        return False
    except:
        return False
