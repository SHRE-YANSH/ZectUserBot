# Copyright (C) 2020-2021 by okay-retard@Github, < https://github.com/okay-retard >.
#
# This file is part of < https://github.com/okay-retard/ZectUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/okay-retard/ZectUserBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import requests
import aiohttp
from pyrogram import filters
from pyrogram.types import Message
from Zect import app, CMD_HELP
from config import PREFIX

CMD_HELP.update(
    {
        "Misc": """
『 **Misc** 』
  `paste` -> Paste replied content to Nekobin.
  `pasty` -> Paste replied content to Pasty.
  `tr` [lang code] -> Transalte a text to a given language.
  `whois` [user handle] -> Provides information about the user.
  `id` [user handle] -> Give user or chat id
"""
    }
)


@app.on_message(
    filters.command(["pasty"], PREFIX) & filters.me
)
async def paste(_, message: Message):
    text = message.reply_to_message.text
    try:
        params = {"content": text}
        headers = {'content-type' : 'application/json'}
        url = "https://pasty.lus.pm/api/v2/pastes/"
        paste = requests.post(url, json=params, headers=headers)
        key = paste.json()["id"]
    except Exception:
        await message.edit_text("`API is down try again later`")
        await asyncio.sleep(2)
        await message.delete()
        return
    else:
        url = f"https://pasty.lus.pm/{key}"
        reply_text = f"**Pasted to: [Pasty]({url})\nRaw link: [Raw]({url}/raw)**"
        delete = (
            True
            if len(message.command) > 1
            and message.command[1] in ["d", "del"]
            and message.reply_to_message.from_user.is_self
            else False
        )
        if delete:
            await asyncio.gather(
                app.send_message(
                    message.chat.id, reply_text, disable_web_page_preview=True
                ),
                message.reply_to_message.delete(),
                message.delete(),
            )
        else:
            await message.edit_text(
                reply_text,
                disable_web_page_preview=True,
            )

@app.on_message(
    filters.command(["neko", "paste"], PREFIX) & filters.me
)
async def neko(_, message: Message):
    text = message.reply_to_message.text
    try:
        params = {"content": text}
        headers = {'content-type' : 'application/json'}
        url = "https://nekobin.com/api/documents"
        neko = requests.post(url, json=params, headers=headers)
        key = neko.json()["result"]["key"]
    except Exception:
        await message.edit_text("`API is down try again later`")
        await asyncio.sleep(2)
        await message.delete()
        return
    else:
        url = f"https://nekobin.com/{key}"
        reply_text = f"**Pasted to: [Nekobin]({url})**"
        delete = (
            True
            if len(message.command) > 1
            and message.command[1] in ["d", "del"]
            and message.reply_to_message.from_user.is_self
            else False
        )
        if delete:
            await asyncio.gather(
                app.send_message(
                    message.chat.id, reply_text, disable_web_page_preview=True
                ),
                message.reply_to_message.delete(),
                message.delete(),
            )
        else:
            await message.edit_text(
                reply_text,
                disable_web_page_preview=True,
            )
