from pyrogram.types import Message, User
from pyrogram import Client
from Zect.database.afkdb import get_afk_status
from Zect.database.pmpermitdb import get_allowed_chat, get_pm_settings, collection
import shlex


def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


def get_args(message):
    try:
        message = message.text
    except AttributeError:
        pass
    if not message:
        return False
    message = message.split(maxsplit=1)
    if len(message) <= 1:
        return []
    message = message[1]
    try:
        split = shlex.split(message)
    except ValueError:
        return message  # Cannot split, let's assume that it's just one long message
    return list(filter(lambda x: len(x) > 0, split))


async def user_afk(filter, client: Client, message: Message):
    check = await get_afk_status()
    if check:
        return True
    else:
        return False


async def denied_users(filter, client: Client, message: Message):
    result = await collection.find_one({"_id": 1})
    if not result:
        return False
    if not result["pmpermit"]:
        return False
    if await get_allowed_chat(message.chat.id):
        return False
    else:
        return True
