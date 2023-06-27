# Copyright (C) 2020-2021 by shre-yansh@Github, < https://github.com/shre-yansh >.
#
# This file is part of < https://github.com/shre-yansh/ZectUserBot > project,
# and is released under the "AGP v3.0 License Agreement".
# Please see < https://github.com/shre-yansh/ZectUserBot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from Zect import app, HELP, CMD_HELP
from config import PREFIX
from Zect.helpers.pyrohelper import get_arg

HELP.update(
    {
        "**Admin Tools**": "__ban, unban, promote, demote, kick, mute, unmute, gmute, ungmute, pin, purge, del, invite__",
        "**AFK**": "__afk, unafk__",
        "**Alive**": "__alive, ping__",
        "**Developer**": "__eval, term, log__",
        "**Filters**": "__filter, filters, stop, stopall__",
        "**Misc**": "__paste, whois, id__",
        "**Notes**": "__save, get, clear, clearall, notes__",
        "**Anti-PM**": "__pmguard, setpmmsg, setlimit, setblockmsg, allow, deny__",
        "**Sticker**": "__kang, stkrinfo__",
        "**Greetings**": "__setwelcome, clearwelcome__",
    }
)


@app.on_message(filters.command("help", PREFIX) & filters.me)
async def help(client, message):
    args = get_arg(message)
    if not args:
        text = "**Available Commands**\n\n"
        for key, value in HELP.items():
            text += f"{key}: {value}\n\n"
        await message.edit(text)
        return
    else:
        module_help = CMD_HELP.get(args, False)
        if not module_help:
            await message.edit("__Invalid module name specified.__")
            return
        else:
            await message.edit(module_help)
