from pyrogram.filters import chat
from . import cli

collection = cli["Zect"]["welcome"]


async def welcome(chat: int, value: bool):
    doc = {"_id": chat, "welcome": value}
    r = await collection.find_one({"_id": chat})
    if r:
        await collection.update_one({"_id": chat}, {"$set": {"welcome": value}})
    else:
        await collection.insert_one(doc)


async def is_welcome(chat_id):
    results = await collection.find_one({"_id": chat_id})
    if not results:
        return False
    else:
        return results["welcome"]


async def set_welcome(chat, welcome_message, media_id):
    await collection.update_one(
        {"_id": chat}, {"$set": {"welcome_msg": welcome_message, "media_id": media_id}}
    )


async def get_welcome(chat):
    r = await collection.find_one({"_id": chat})
    is_media = False
    if r["media_id"]:
        is_media = True
        return is_media, r["media_id"]
    else:
        return is_media, r["welcome_msg"]
