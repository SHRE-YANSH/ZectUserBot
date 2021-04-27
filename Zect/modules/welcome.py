# Copyright (C) 2020-2021 by okay-retard@Github, < https://github.com/okay-retard >.
#
# This file is part of < https://github.com/okay-retard/ZectUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/okay-retard/ZectUserBot/blob/master/LICENSE >
#
# All rights reserved.

import re
from pyrogram import filters

from Zect import app, CMD_HELP
from Zect.helpers.pyrohelper import get_arg, welcome_chat
import Zect.database.welcomedb as Zectdb
from config import PREFIX, LOG_CHAT


CMD_HELP.update(
    {
        "Greetings": """
『 **Greetings** 』
  `setwelcome` -> Sets a custom welcome message.
  `clearwelcome` -> Disables welcome message in the chat.
  """
    }
)

LOG_CHAT = LOG_CHAT


@app.on_message(filters.command("clearwelcome", PREFIX) & filters.me)
async def welcome(client, message):
    await Zectdb.clear_welcome(str(message.chat.id))
    await message.edit("**I am sulking not to say hello anymore :(**")


@app.on_message(filters.create(welcome_chat) & filters.new_chat_members, group=-2)
async def new_welcome(client, message):
    msg_id = await Zectdb.get_welcome(str(message.chat.id))
    caption = ""
    men = ""
    msg = await app.get_messages(LOG_CHAT, msg_id)
    if msg.media:
        if msg.caption:
            caption = msg.caption
            if "{mention}" in caption:
                men = caption.replace("{mention}", "[{}](tg://user?id={})")
        if msg.photo and caption is not None:
            await app.send_photo(
                message.chat.id,
                msg.photo.file_id,
                caption=men.format(
                    message.new_chat_members[0]["first_name"],
                    message.new_chat_members[0]["id"],
                ),
                reply_to_message_id=message.message_id,
            )
        if msg.animation and caption is not None:
            await app.send_animation(
                message.chat.id,
                msg.animation.file_id,
                caption=men.format(
                    message.new_chat_members[0]["first_name"],
                    message.new_chat_members[0]["id"],
                ),
                reply_to_message_id=message.message_id,
            )
        if msg.sticker:
            await app.send_sticker(
                message.chat.id,
                msg.sticker.file_id,
                reply_to_message_id=message.message_id,
            )

    else:
        text = msg.text
        if "{mention}" in text:
            men = text.replace("{mention}", "[{}](tg://user?id={})")
            await app.send_message(
                message.chat.id,
                men.format(
                    message.new_chat_members[0]["first_name"],
                    message.new_chat_members[0]["id"],
                ),
                reply_to_message_id=message.message_id,
            )
        else:
            await app.send_message(
                message.chat.id, text, reply_to_message_id=message.message_id
            )


@app.on_message(filters.command("setwelcome", PREFIX) & filters.me)
async def setwelcome(client, message):
    reply = message.reply_to_message
    if not reply:
        await message.edit("**Reply to a message or media to set welcome message.**")
        return
    frwd = await app.copy_message(LOG_CHAT, message.chat.id, reply.message_id)
    msg_id = frwd.message_id
    await Zectdb.save_welcome(str(message.chat.id), msg_id)
    await message.edit("**Welcome message has been saved.**")
