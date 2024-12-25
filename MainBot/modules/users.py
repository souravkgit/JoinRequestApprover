from MainBot import (
    application,
    VALID_CHAT_IDS,
    DEFAULT_WELCOME_MESSAGE,
    FIRST_NAMES,
    DEFAULT_LEAVE_MSG,
    CURRENT_USERS,
    LOGGER,
)
import MainBot.modules.mongo.extra_stuff as extra_stuff
from telegram.ext import ChatJoinRequestHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
import MainBot.modules.mongo.users as userss
from telegram.helpers import escape_markdown, mention_markdown
from telegram.constants import ParseMode


async def handle_chat_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global VALID_CHAT_IDS
    chat = update.effective_chat
    user = update.effective_user
    await log_user(user)
    if str(chat.id) not in VALID_CHAT_IDS:
        return
    user_id = str(user.id)
    try:
        try:
            first_name = user.first_name or "PersonWithNoFirstName"
            last_name = user.last_name or "PersonWithNoLastName"
            if user.last_name:
                fullname = escape_markdown(f"{first_name} {user.last_name}")
            else:
                fullname = escape_markdown(first_name)
            count = await chat.get_member_count()
            mention = mention_markdown(user.id, escape_markdown(first_name))
            if user.username:
                username = "@" + escape_markdown(user.username)
            else:
                username = mention
            msg_ = DEFAULT_WELCOME_MESSAGE.format(
                first=escape_markdown(first_name),
                chatname=escape_markdown(chat.title),
                last=escape_markdown(last_name),
                fullname=escape_markdown(fullname),
                username=escape_markdown(username),
                id=user.id,
                count=count,
                mention=mention,
            )
            await user.send_message(msg_, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            LOGGER.info(f"Error in new member : {str(e)}")
        await update.chat_join_request.approve()
    except Exception as e:
        LOGGER.info(f"Error in handle chat join request : {str(e)}")
    await userss.add_user_chat(user_id, str(chat.id))


async def left_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    global VALID_CHAT_IDS
    bot = context.bot
    chat = update.effective_chat
    left_user = update.message.left_chat_member
    if left_user:
        if left_user.id == bot.id:
            try:
                VALID_CHAT_IDS.remove(str(chat.id))
            except:
                pass
            await extra_stuff.remove_valid_chat(str(chat.id))
        else:
            try:
                user = left_user
                first_name = user.first_name or "PersonWithNoFirstName"
                last_name = user.last_name or "PersonWithNoLastName"
                if user.last_name:
                    fullname = escape_markdown(f"{first_name} {user.last_name}")
                else:
                    fullname = escape_markdown(first_name)
                count = await chat.get_member_count()
                mention = mention_markdown(user.id, escape_markdown(first_name))
                if user.username:
                    username = "@" + escape_markdown(user.username)
                else:
                    username = mention
                msg_ = DEFAULT_LEAVE_MSG.format(
                    first=escape_markdown(first_name),
                    chatname=escape_markdown(chat.title),
                    last=escape_markdown(last_name),
                    fullname=escape_markdown(fullname),
                    username=escape_markdown(username),
                    id=user.id,
                    count=count,
                    mention=mention,
                )
                print(user.id)
                await left_user.send_message(msg_, parse_mode=ParseMode.MARKDOWN)
                # await context.bot.send_message(
                #     user.id, msg_, parse_mode=ParseMode.MARKDOWN
                # )
            except Exception as e:
                LOGGER.info(f"Error in left member : {str(e)}")


async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    print("bot added me aaya")
    global VALID_CHAT_IDS
    bot = context.bot
    chat = update.effective_chat
    msg = update.effective_message
    if msg.new_chat_members:
        chat_id = str(chat.id)
        new_members = update.effective_message.new_chat_members
        for new_mem in new_members:
            if new_mem.id == bot.id:
                print("bot added")
                VALID_CHAT_IDS.add(chat_id)
                await extra_stuff.add_valid_chat(chat_id)


async def log_user(user):
    global CURRENT_USERS, FIRST_NAMES
    user_id = str(user.id)
    await userss.set_user(
        user_id,
        user.first_name,
        user.last_name,
        user.username,
    )
    CURRENT_USERS.add(user_id)
    FIRST_NAMES[user_id] = user.first_name


REMOVE_CHANNEL_AUTOMATIC_HANDLER = MessageHandler(
    filters.StatusUpdate.LEFT_CHAT_MEMBER, left_member
)
ADD_CHANNEL_AUTOMATIC_HANDLER = MessageHandler(
    filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member
)

CHAT_JOIN_REQUEST_HANDLER = ChatJoinRequestHandler(
    handle_chat_join_request, block=False
)
application.add_handler(REMOVE_CHANNEL_AUTOMATIC_HANDLER)
application.add_handler(ADD_CHANNEL_AUTOMATIC_HANDLER)
application.add_handler(CHAT_JOIN_REQUEST_HANDLER)

__mod_name__ = "users"
__handlers__ = [
    CHAT_JOIN_REQUEST_HANDLER,
    REMOVE_CHANNEL_AUTOMATIC_HANDLER,
    ADD_CHANNEL_AUTOMATIC_HANDLER,
]
