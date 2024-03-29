# Copyright (C) 2020-2021 by okay-retard@Github, < https://github.com/okay-retard >.
#
# This file is part of < https://github.com/okay-retard/ZectUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/okay-retard/ZectUserBot/blob/master/LICENSE >
#
# All rights reserved.

import math
from datetime import datetime
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram import enums
from inspect import getfullargspec
from Zect import app
from Zect.helpers.adminhelpers import CheckAdmin
from config import PREFIX


async def edrep(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})




@app.on_message(filters.command("purge", ".") & filters.me)
async def purge_message(client, message):
    chat_type  = [enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL]
    if message.chat.type in chat_type:
        is_admin = await CheckAdmin(message)
        if not is_admin:
            await message.delete()
            return
    else:
        pass
    start_t = datetime.now()
    await message.delete()
    message_ids = []
    count_del_etion_s = 0
    if message.reply_to_message:
        for a_s_message_id in range(
            message.reply_to_message.id, message.id
        ):
            message_ids.append(a_s_message_id)
            if len(message_ids) == 100:
                await client.delete_messages(
                    chat_id=message.chat.id, message_ids=message_ids, revoke=True
                )
                count_del_etion_s += len(message_ids)
                message_ids = []
        if message_ids:
            await client.delete_messages(
                chat_id=message.chat.id, message_ids=message_ids, revoke=True
            )
            count_del_etion_s += len(message_ids)
    end_t = datetime.now()
    time_taken_ms = (end_t - start_t).seconds
    ms_g = await client.send_message(
        message.chat.id,
        f"Purged {count_del_etion_s} messages in {time_taken_ms} seconds",
    )
    await asyncio.sleep(5)
    await ms_g.delete()


@app.on_message(filters.command("del", ".") & filters.me)
async def delete_replied(client, message):
    msg_ids = [message.message_id]
    if message.reply_to_message:
        msg_ids.append(message.reply_to_message.message_id)
    await client.delete_messages(message.chat.id, msg_ids)
