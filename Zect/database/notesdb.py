# Copyright (C) 2020-2021 by okay-retard@Github, < https://github.com/okay-retard >.
#
# This file is part of < https://github.com/okay-retard/ZectUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/okay-retard/ZectUserBot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram.filters import chat
from . import cli

collection = cli["Zect"]["notes"]


async def save_note(note_name, note_id):
    doc = {"_id": 1, "notes": {note_name: note_id}}
    result = await collection.find_one({"_id": 1})
    if result:
        await collection.update_one(
            {"_id": 1}, {"$set": {f"notes.{note_name}": note_id}}
        )
    else:
        await collection.insert_one(doc)


async def get_note(note_name):
    result = await collection.find_one({"_id": 1})
    if result is not None:
        try:
            note_id = result["notes"][note_name]
            return note_id
        except KeyError:
            return None
    else:
        return None


async def rm_note(note_name):
    await collection.update_one({"_id": 1}, {"$unset": {f"notes.{note_name}": ""}})


async def all_notes():
    results = await collection.find_one({"_id": 1})
    try:
        notes_dic = results["notes"]
        key_list = notes_dic.keys()
        return key_list
    except:
        return None


async def rm_all():
    await collection.update_one({"_id": 1}, {"$unset": {"notes": ""}})
