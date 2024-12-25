class Config(object):
    TOKEN = ""  # Get bot token from bot father
    DB_URI = "mongodb+srv://*****:******@*******.9wgb5ar.mongodb.net/JoinRequestApprovalRoBot?retryWrites=true&w=majority"  # mongodb uri from mongodb
    BOT_USERNAME = ""  # Bot username
    VALID_CHAT_IDS = set([])  # Default channels to work in
    OWNER_ID = "1608141072"  # Owner ID
    OWNER_USERNAME = "goyalcompany"  # Owner username
    DEV_USERNAME = "PythonDeveloperHub"
    ADMINS = set(["1608141072"])  # Default admins
    USER_LOCKS = {}  # Owner ID
    ERROR_LOGS = -10000000000  # Error logger chat id
    FIRST_NAMES = {}
    CURRENT_USERS = set([])
    VALID_WELCOME_FORMATTERS = [
        "first",
        "last",
        "fullname",
        "username",
        "id",
        "count",
        "chatname",
        "mention",
    ]
    DEFAULT_WELCOME_MESSAGE = (
        "Hey {first}! Welcome to the chat {chatname}."  # Default welcome message
    )
    DEFAULT_LEAVE_MSG = (
        "Hey {first}!, You just left the chat {chatname}"  # Default goodbye message
    )


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
