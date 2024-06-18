# Copyright (C) 2020-2021 by shre-yansh@Github, < https://github.com/shre-yansh >.
#
# This file is part of < https://github.com/shre-yansh/ZectUserBot > project,
# and is released under the "AGP v3.0 License Agreement".
# Please see < https://github.com/shre-yansh/ZectUserBot/blob/master/LICENSE >
#
# All rights reserved.

import logging
import sys
import time
from pyrogram import Client, errors
from config import API_HASH, API_ID
try:
    from config import SESSION
except ImportError:
    SESSION = None
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [Zect] - %(levelname)s - %(message)s",
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("apscheduler").setLevel(logging.ERROR)

HELP = {}
CMD_HELP = {}

StartTime = time.time()

if SESSION:
    app = Client("zect", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
else:
    app = Client("zect", api_id=API_ID, api_hash=API_HASH)
