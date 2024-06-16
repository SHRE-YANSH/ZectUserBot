# Copyright (C) 2020-2021 by shre-yansh@Github, < https://github.com/shre-yansh >.
#
# This file is part of < https://github.com/shre-yansh/ZectUserBot > project,
# and is released under the "AGP v3.0 License Agreement".
# Please see < https://github.com/shre-yansh/ZectUserBot/blob/master/LICENSE >
#
# All rights reserved.

from . import cli

filter = cli["Zect"]["loader"]


async def save_module(name, url) -> None:
    add = await filter.find_one({"name": name})
    if add:
        await filter.update_one(
            {"name": name},
            {"$set": {"raw_url": url,}},
        )
    else:
        await filter.insert_one(
            {"name": name, "raw_url": url}
        )


async def del_module(name):
    delete = await filter.find_one({"name": name})
    if delete:
        await filter.delete_one(delete)
    else:
        return False


async def all_modules():
    r = [jo async for jo in filter.find({})]
    if r:
        return r
    else:
        return False
