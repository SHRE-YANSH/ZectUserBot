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

app.start()
me = app.get_me()
print(f"Zect UserBot started for user {me.id}. Type {PREFIX}help in any telegram chat.")
idle()
