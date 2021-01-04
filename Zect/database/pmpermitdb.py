from pymongo import settings
from . import cli

collection = cli["Zect"]["pmpermit"]


PMPERMIT_MESSAGE = (
    "`Ok! Stop Right there Read this first before sending any new messages.\n\n`"
    "`I'm a bot Protecting this user's PM from any kind of Spam.`"
    "`Please wait for my Master to come back Online.\n\n`"
    "`Until then, Don't spam, Or you'll get blocked and reported!`"
)

BLOCKED = "`Guess You're A Spammer, Blocked Successfully `"

LIMIT = 5

doc = {"_id": 1, "pmpermit": False}
r = collection.find_one({"_id": 1})
if r:
    pass
else:
    collection.insert_one(doc)


def set_pm(value: bool):
    collection.update_one({"_id": 1}, {"$set": {"pmpermit": value}})


def set_permit_message(text):
    collection.update_one({"_id": 1}, {"$set": {"pmpermit_message": text}})


def set_block_message(text):
    collection.update_one({"_id": 1}, {"$set": {"block_message": text}})


def set_limit(limit):
    collection.update_one({"_id": 1}, {"$set": {"limit": limit}})


def get_pm_settings():
    result = collection.find_one({"_id": 1})
    pmpermit = result["pmpermit"]
    pm_message = result.get("pmpermit_message", PMPERMIT_MESSAGE)
    block_message = result.get("block_message", BLOCKED)
    limit = result.get("limit", LIMIT)
    return pmpermit, pm_message, limit, block_message


def allow_deny(chat, value):
    collection.update_one({"_id": chat}, {"$set": {"allow": value}})


def get_allowed_chat(chat):
    pm_on, msg, limit, block_msg = get_pm_settings()
    if pm_on:
        doc = {"_id": chat, "allow": False}
    else:
        doc = {"_id": chat, "allow": True}
    r = collection.find_one({"_id": chat})
    if not r:
        collection.insert_one(doc)
    else:
        return r["allow"]
