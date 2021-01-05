from pyrogram.filters import chat
from . import cli

collection = cli["Zect"]["welcome"]


def welcome(chat: int, value: bool):
    doc = {"_id": chat, "welcome": value}
    r = collection.find_one({"_id": chat})
    if r:
        collection.update_one({"_id": chat}, {"$set": {"welcome": value}})
    else:
        collection.insert_one(doc)


def get_welcome_chat():
    chats = []
    results = collection.find({"welcome": True})
    for result in results:
        chats.append(result["_id"])
    return chats


def set_welcome(chat, welcome_message, media_id):
    collection.update_one(
        {"_id": chat}, {"$set": {"welcome_msg": welcome_message, "media_id": media_id}}
    )


def get_welcome(chat):
    r = collection.find_one({"_id": chat})
    is_media = False
    try:
        if r["media_id"]:
            is_media = True
            return is_media, r["media_id"], True
        else:
            return is_media, r["welcome_msg"], True
    except:
        return None, None, False
