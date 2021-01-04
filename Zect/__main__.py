from pyrogram import idle, Client
from Zect import app, LOGGER
from Zect.modules import *

app.start()
LOGGER.info("Your Zect UserBot is ready for use type .help in any telegram chat.")
idle()
