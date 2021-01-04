
from pymongo import settings
from .import cli

collection = cli["Zect"]["pmpermit"]


PMPERMIT_MESSAGE = (
    "`Hello! This is an automated message.\n\n`"
    "`I haven't approved you to PM yet.`"
    "`Please wait for me to look in, I mostly approve PMs.\n\n`"
    "`Until then, please don't spam my PM, you'll get blocked and reported!`")

BLOCKED = "`I don't want any PM from so you have been blocked !`"

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
    limit = result.get('limit', LIMIT)
    return pmpermit, pm_message, limit


def allow_deny(chat, value):
    collection.update_one({"_id": chat}, {"$set": {"allow": value, "pms": 0}})


def get_allowed_chat(chat):
    pm_on, msg, limit = get_pm_settings()
    if pm_on:
        doc = {"_id": chat, "allow": False, "pms": 0}
    else:
        doc = {"_id": chat, "allow": True, "pms": 0}
    r = collection.find_one({"_id": chat})
    if not r:
        collection.insert_one(doc)
    else:
        return r["allow"]
