from pyrogram.types import Message, User
from pyrogram import Client
from Zect.database.afkdb import get_afk_status
from Zect.database.pmpermitdb import get_allowed_chat, get_pm_settings


def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


async def user_afk(filter, client: Client, message: Message):
    check = await get_afk_status()
    if check:
        return True
    else:
        return False


async def denied_users(filter, client: Client, message: Message):
    pmpermit, pm_message, limit, block_msg = await get_pm_settings()
    if not pmpermit:
        return False
    if await get_allowed_chat(message.chat.id):
        return False
    else:
        return True
