from . import cli
import asyncio

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


async def set_pm(value: bool):
    await collection.update_one({"_id": 1}, {"$set": {"pmpermit": value}})


async def set_permit_message(text):
    await collection.update_one({"_id": 1}, {"$set": {"pmpermit_message": text}})


async def set_block_message(text):
    await collection.update_one({"_id": 1}, {"$set": {"block_message": text}})


async def set_limit(limit):
    await collection.update_one({"_id": 1}, {"$set": {"limit": limit}})


async def get_pm_settings():
    result = await collection.find_one({"_id": 1})
    if not result:
        return
    pmpermit = result["pmpermit"]
    pm_message = result.get("pmpermit_message", PMPERMIT_MESSAGE)
    block_message = result.get("block_message", BLOCKED)
    limit = result.get("limit", LIMIT)
    return pmpermit, pm_message, limit, block_message


async def allow_deny(chat, value):
    await collection.update_one({"_id": chat}, {"$set": {"allow": value}})


async def get_allowed_chat(chat):
    pm_on, msg, limit, block_msg = await get_pm_settings()
    if pm_on:
        doc = {"_id": chat, "allow": False}
    else:
        doc = {"_id": chat, "allow": True}
    r = await collection.find_one({"_id": chat})
    if not r:
        await collection.insert_one(doc)
    else:
        return r["allow"]
