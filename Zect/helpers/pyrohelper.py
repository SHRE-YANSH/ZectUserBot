from pyrogram.types import Message, User
from pyrogram import Client
from Zect.database.afkdb import get_afk_status
from Zect.database.pmpermitdb import get_allowed_chat, get_pm_settings


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
