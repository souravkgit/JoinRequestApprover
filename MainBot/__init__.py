import logging
import sys
import time
from telegram.ext import Application

StartTime = time.time()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)


from MainBot.configs import Development as Config

TOKEN = Config.TOKEN
DB_URI = Config.DB_URI
ADMINS = Config.ADMINS
VALID_CHAT_IDS = Config.VALID_CHAT_IDS
OWNER_ID = Config.OWNER_ID
ADMINS.add(OWNER_ID)
ERROR_LOGS = Config.ERROR_LOGS
BOT_USERNAME = Config.BOT_USERNAME
DEV_USERNAME = Config.DEV_USERNAME
OWNER_USERNAME = Config.OWNER_USERNAME
CURRENT_USERS = Config.CURRENT_USERS
FIRST_NAMES = Config.FIRST_NAMES
VALID_WELCOME_FORMATTERS = Config.VALID_WELCOME_FORMATTERS
DEFAULT_WELCOME_MESSAGE = Config.DEFAULT_WELCOME_MESSAGE
DEFAULT_LEAVE_MSG = Config.DEFAULT_LEAVE_MSG
application = Application.builder().token(TOKEN).build()
JOB_QUEUE = application.job_queue
