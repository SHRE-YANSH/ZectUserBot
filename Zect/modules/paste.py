# Copyright (C) 2020-2021 by shre-yansh@Github, < https://github.com/shre-yansh >.
#
# This file is part of < https://github.com/shre-yansh/ZectUserBot > project,
# and is released under the "AGP v3.0 License Agreement".
# Please see < https://github.com/shre-yansh/ZectUserBot/blob/master/LICENSE >
#

        
import asyncio
import os
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
  `whois` [user handle] -> Provides information about the user.
  `id` [user handle] -> Give user or chat id
"""
    }
)

def paste(text):
    try:
        data = {"content": text, "extension": "txt"}
        url = "https://spaceb.in/api/v1/documents"
        neko = requests.post(url, data=data)
        data = neko.json()
    except Exception as e:
        return False
    else:
        id = data["payload"]["id"]
        # id = f'https://spaceb.in/{data["payload"]["id"]}'
        return id
@app.on_message(
    filters.command(["paste"], PREFIX) & filters.me
)
async def neko(_, message: Message):
    if message.reply_to_message.text:
        text = message.reply_to_message.text
    elif message.reply_to_message.document:
        file = await app.download_media(message.reply_to_message.document.file_id)
        with open(file, "r") as f:
            text = f.read()
        os.remove(file)
    else:
        await message.edit_text("`Reply to a text or document file`")
        return
    id = paste(text)
    url = f'https://spaceb.in/{id}'
    raw_url = f'https://spaceb.in/api/v1/documents/{id}/raw'
    if not url:
        await message.edit_text("`API is down try again later`")
        await asyncio.sleep(2)
        await message.delete()
        return
    else:
        reply_text = f"**Pasted to: [Sbacebin]({url})\nRaw Url: [Raw]({raw_url})**"
       
        await message.edit_text(
            reply_text,
            disable_web_page_preview=True,
        )
