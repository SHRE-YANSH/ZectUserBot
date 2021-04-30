# Copyright (C) 2020-2021 by okay-retard@Github, < https://github.com/okay-retard >.
#
# This file is part of < https://github.com/okay-retard/ZectUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/okay-retard/ZectUserBot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import idle, Client, filters
from config import PREFIX
from Zect import app, LOGGER
import logging
from Zect.modules import *

app.start()
me = app.get_me()
print(f"Zect UserBot started for user {me.id}. Type {PREFIX}help in any telegram chat.")
idle()
