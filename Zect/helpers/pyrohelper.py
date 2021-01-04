from pyrogram.types import Message, User
from pyrogram import Client
from Zect.database.afkdb import get_afk_status
from Zect.database.pmpermitdb import get_allowed_chat, get_pm_settings


def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


def SpeedConvert(size):
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kbit/s", 2: "Mbit/s", 3: "Gbit/s", 4: "Tbit/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


def GetFromUserID(message: Message):
    """ Get the user id of the incoming message."""
    return message.from_user.id


def GetChatID(message: Message):
    """ Get the group id of the incoming message"""
    return message.chat.id


def GetUserMentionable(user: User):
    """ Get mentionable text of a user."""
    if user.username:
        username = "@{}".format(user.username)
    else:
        if user.last_name:
            name_string = "{} {}".format(user.first_name, user.last_name)
        else:
            name_string = "{}".format(user.first_name)

        username = "<a href='tg://user?id={}'>{}</a>".format(
            user.id, name_string)

    return username


def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


async def user_afk(filter, client: Client, message: Message):
    check = get_afk_status()
    if check:
        return True
    else:
        return False


async def denied_users(filter, client: Client, message: Message):
    pmpermit, pm_message, limit = get_pm_settings()
    if not pmpermit:
        return False
    if get_allowed_chat(message.chat.id):
        return False
    else:
        return True
