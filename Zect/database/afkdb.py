# Copyright (C) 2020-2021 by shre-yansh@Github, < https://github.com/shre-yansh >.
#
# This file is part of < https://github.com/shre-yansh/ZectUserBot > project,
# and is released under the "AGP v3.0 License Agreement".
# Please see < https://github.com/shre-yansh/ZectUserBot/blob/master/LICENSE >
#
# All rights reserved.

from . import cli
import asyncio

collection = cli["Zect"]["afk"]


async def set_afk(afk_status, afk_since, reason):
    doc = {"_id": 1, "afk_status": afk_status}
    r = await collection.find_one({"_id": 1})
    if r:
        await collection.update_one(
            {"_id": 1},
            {
                "$set": {
                    "afk_status": afk_status,
                    "afk_since": afk_since,
                    "reason": reason,
                }
            },
        )
    else:
        await collection.insert_one(doc)


async def set_unafk():
    await collection.update_one(
        {"_id": 1}, {"$set": {"afk_status": False, "afk_since": None, "reason": None}}
    )


async def get_afk_status():
    result = await collection.find_one({"_id": 1})
    if not result:
        return False
    else:
        status = result["afk_status"]
        return status


async def afk_stuff():
    result = await collection.find_one({"_id": 1})
    afk_since = result["afk_since"]
    reason = result["reason"]
    return afk_since, reason
