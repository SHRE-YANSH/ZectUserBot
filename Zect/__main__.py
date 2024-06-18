# Copyright (C) 2020-2021 by shre-yansh@Github, < https://github.com/shre-yansh >.
#
# This file is part of < https://github.com/shre-yansh/ZectUserBot > project,
# and is released under the "AGP v3.0 License Agreement".
# Please see < https://github.com/shre-yansh/ZectUserBot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import idle, Client, filters
from config import PREFIX
from Zect import app
import logging
from Zect.modules import *
from urllib.parse import urlparse
from Zect.helpers.pyrohelper import load_module
import os


async def start():
    await app.start()
    me = await app.get_me()
    logging.info("Deploying Zect UserBot...")
    logging.info(f"Checking for external modules...")
    await load_module()
    logging.info(f"Zect UserBot started for user {me.id}. Type {PREFIX}help in any telegram chat.")
    try:
        with open('temp_message_id.txt', 'r') as f:
            data_string = f.read()
    except FileNotFoundError:
        data_string = ""
    if data_string:
        chat_id, message_id = data_string.split(',')
        await app.edit_message_text(int(chat_id), int(message_id), "Zect UserBot has been restarted successfully.")
        os.remove('temp_message_id.txt')
    await idle()

app.loop.run_until_complete(start())

