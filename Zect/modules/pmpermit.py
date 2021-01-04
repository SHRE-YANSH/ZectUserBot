from pyrogram import filters
import asyncio

from pyrogram.methods import messages
from Zect import app, CMD_HELP
from Zect.helpers.pyrohelper import get_arg, denied_users
import Zect.database.pmpermitdb as Zectdb
from config import PREFIX

CMD_HELP.update(
    {
        "Anti-PM": """
『 **Anti-PM** 』
  `pmgaurd` [on or off] -> Activates or deactivates anti-pm.
  `setpmmsg` [message or default] -> Sets a custom anti-pm message.
  `setblockmsg` [message or default] -> Sets custom block message.
  `setlimit` [value] -> This one sets a max. message limit for unwanted PMs and when they go beyond it, bamm!.
  `allow` -> Allows a user to PM you.
  `deny` -> Denies a user to PM you.
  """
    }
)

FLOOD_CTRL = 0
ALLOWED = []
USERS_AND_WARNS = {}


@app.on_message(filters.command("pmgaurd", PREFIX) & filters.me)
async def pmgaurd(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**I only understand on or off**")
        return
    if arg == "off":
        Zectdb.set_pm(False)
        await message.edit("**PM Gaurd Deactivated**")
    if arg == "on":
        Zectdb.set_pm(True)
        await message.edit("**PM Gaurd Activated**")


@app.on_message(filters.command("setlimit", PREFIX) & filters.me)
async def pmgaurd(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Set limit to what?**")
        return
    Zectdb.set_limit(int(arg))


@app.on_message(filters.command("setpmmsg", PREFIX) & filters.me)
async def setpmmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**What message to set**")
        return
    if arg == "default":
        Zectdb.set_permit_message(Zectdb.PMPERMIT_MESSAGE)
        await message.edit("**Anti_PM message set to default**.")
        return
    Zectdb.set_permit_message(f"`{arg}`")
    await message.edit("**Custom anti-pm message set**")


@app.on_message(filters.command("setblockmsg", PREFIX) & filters.me)
async def setpmmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**What message to set**")
        return
    if arg == "default":
        Zectdb.set_permit_message(Zectdb.BLOCKED)
        await message.edit("**Block message set to default**.")
        return
    Zectdb.set_permit_message(f"`{arg}`")
    await message.edit("**Custom block message set**")


@app.on_message(filters.command("allow", PREFIX) & filters.me & filters.private)
async def allow(client, message):
    chat_id = message.chat.id
    Zectdb.allow_deny(chat_id, True)
    await message.edit(f"**I have allowed [you](tg://user?id={chat_id}) to PM me.**")


@app.on_message(filters.command("deny", PREFIX) & filters.me & filters.private)
async def deny(client, message):
    chat_id = message.chat.id
    Zectdb.allow_deny(chat_id, False)
    await message.edit(f"**I have denied [you](tg://user?id={chat_id}) to PM me.**")


@app.on_message(
    filters.private & filters.incoming & filters.create(denied_users) & ~filters.me
)
async def reply_pm(client, message):
    global FLOOD_CTRL
    pmpermit, pm_message, limit, block_message = Zectdb.get_pm_settings()
    user = message.from_user.id
    user_warns = 0 if user not in USERS_AND_WARNS else USERS_AND_WARNS[user]
    if user_warns <= await limit - 2:
        user_warns += 1
        USERS_AND_WARNS.update({user: user_warns})
        if not FLOOD_CTRL > 0:
            FLOOD_CTRL += 1
        else:
            FLOOD_CTRL = 0
            return
        async for message in await app.search_messages(
            chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
        ):
            await message.delete()
        await message.reply(pm_message, disable_web_page_preview=True)
        return
    await message.reply(block_message, disable_web_page_preview=True)
    await app.block_user(message.chat.id)
    USERS_AND_WARNS.update({user: 0})
