import logging
import sys
import time
from pyrogram import Client, errors
from config import API_HASH, API_ID, SESSION
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


LOGGER = logging.getLogger(__name__)

HELP = {}
CMD_HELP = {}

StartTime = time.time()

API_ID = API_ID
API_HASH = API_HASH
SESSION = SESSION

app = Client(SESSION, api_id=API_ID, api_hash=API_HASH)
