# Copyright (C) 2020-2021 by shre-yansh@Github, < https://github.com/shre-yansh >.
#
# This file is part of < https://github.com/shre-yansh/ZectUserBot > project,
# and is released under the "AGP v3.0 License Agreement".
# Please see < https://github.com/shre-yansh/ZectUserBot/blob/master/LICENSE >
#
# All rights reserved.

import time
import asyncio
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions, ChatPrivileges

from pyrogram.errors import UserAdminInvalid

from Zect import app, CMD_HELP
from pyrogram import enums
from Zect.helpers.pyrohelper import get_arg, get_args
from Zect.helpers.adminhelpers import CheckAdmin
from config import PREFIX

CMD_HELP.update(
    {
        "Admin Tools": """
『 **Admin Tools** 』
  `ban` -> Bans user indefinitely.
  `unban` -> Unbans the user.
  `promote` [optional title] -> Promotes a user.
  `demote` _> Demotes a user.
  `mute` -> Mutes user indefinitely.
  `unmute` -> Unmutes the user.
  `kick` -> Kicks the user out of the group.
  `gmute` -> Doesn't lets a user speak(even admins).
  `ungmute` -> Inverse of what gmute does.
  `pin` -> pins a message.
  `del` -> delete a message.
  `purge` -> purge message(s)
  `invite` -> add user to chat.
"""
    }
)


@app.on_message(filters.command("ban", PREFIX) & filters.me)
async def ban_hammer(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user.id
        else:
            user = get_arg(message)
            if not user:
                await message.edit("**I can't ban no-one, can I?**")
                return
        try:
            get_user = await app.get_users(user)
            await app.ban_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
            )
            await message.edit(f"**Banned {get_user.first_name} from the chat.**")
        except:
            await message.edit("**I can't ban this user.**")
    else:
        await message.edit("**Am I an admin here?**")


@app.on_message(filters.command("unban", PREFIX) & filters.me)
async def unban(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user.id
        else:
            user = get_arg(message)
            if not user:
                await message.edit("**I need someone to be unbanned here.**")
                return
        try:
            get_user = await app.get_users(user)
            await app.unban_chat_member(chat_id=message.chat.id, user_id=get_user.id)
            await message.edit(f"**Unbanned {get_user.first_name} from the chat.**")
        except:
            await message.edit("**I can't unban this user.**")
    else:
        await message.edit("**Am I an admin here?**")


# Mute Permissions
mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_send_polls=False,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@app.on_message(filters.command("mute", PREFIX) & filters.me)
async def mute_hammer(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user.id
        else:
            user = get_arg(message)
            if not user:
                await message.edit("**I can't mute no-one, can I?**")
                return
        try:
            get_user = await app.get_users(user)
            await app.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
                permissions=mute_permission,
            )
            await message.edit(f"**{get_user.first_name} has been muted.**")
        except:
            await message.edit("**I can't mute this user.**")
    else:
        await message.edit("**Am I an admin here?**")


# Unmute permissions
unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_send_polls=True,
    can_change_info=False,
    can_pin_messages=False,
)


@app.on_message(filters.command("unmute", PREFIX) & filters.me)
async def unmute(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user.id
        else:
            user = get_arg(message)
            if not user:
                await message.edit("**Whome should I unmute?**")
                return
        try:
            get_user = await app.get_users(user)
            await app.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
                permissions=unmute_permissions,
            )
            await message.edit(f"**{get_user.first_name} was unmuted.**")
        except:
            await message.edit("**I can't unmute this user.**")
    else:
        await message.edit("**Am I an admin here?**")


@app.on_message(filters.command("kick", PREFIX) & filters.me)
async def kick_user(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user.id
        else:
            user = get_arg(message)
            if not user:
                await message.edit("**Whome should I kick?**")
                return
        try:
            get_user = await app.get_users(user)
            await app.ban_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
            )
            await app.unban_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
            )
            await message.edit(f"**Kicked {get_user.first_name} from the chat.**")
        except:
            await message.edit("**I can't kick this user.**")
    else:
        await message.edit("**Am I an admin here?**")


@app.on_message(filters.command("pin", PREFIX) & filters.me)
async def pin_message(_, message: Message):
    chat_type  = [enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL]
    if message.chat.type in chat_type:
        if await CheckAdmin(message=message):
            # If you replied to a message so that we can pin it.
            if message.reply_to_message:
                disable_notification = True

                # Let me see if you want to notify everyone. People are gonna hate you for this...
                if len(message.command) >= 2 and message.command[1] in [
                    "alert",
                    "notify",
                    "loud",
                ]:
                    disable_notification = False

                # Pin the fucking message.
                await app.pin_chat_message(
                    message.chat.id,
                    message.reply_to_message.id,
                    disable_notification=disable_notification,
                )
                await message.edit("`Pinned message!`")
            else:
                # You didn't reply to a message and we can't pin anything. ffs
                await message.edit(
                    "`Reply to a message so that I can pin the god damned thing...`"
                )
        else:
            # You have no business running this command.
            await message.edit("`I am not an admin here lmao. What am I doing?`")
    else:
        # Are you fucking dumb this is not a group ffs.
        await message.edit("`This is not a place where I can pin shit.`")

    # And of course delete your lame attempt at changing the group picture.
    # RIP you.
    # You're probably gonna get ridiculed by everyone in the group for your failed attempt.
    # RIP.
    await asyncio.sleep(3)
    await message.delete()


@app.on_message(filters.command("promote", PREFIX) & filters.me)
async def promote(client, message: Message):
    if await CheckAdmin(message) is False:
        await message.edit("**Am I an admin here?.**")
        return
    title = "Admin"
    reply = message.reply_to_message
    if reply:
        user = reply.from_user.id
        title = str(get_arg(message))
    else:
        args = get_args(message)
        if not args:
            await message.edit("**I can't promote no-one, can I?**")
            return
        user = args[0]
        if len(args) > 1:
            title = " ".join(args[1:])
    get_user = await app.get_users(user)
    try:
        await app.promote_chat_member(message.chat.id, user, ChatPrivileges(
            can_delete_messages=True,
            can_manage_chat=True,
            can_invite_users=True,
            can_change_info=False,
            can_pin_messages=True,
            can_restrict_members=True
            ))
        await message.edit(
            f"**{get_user.first_name} is now powered with admin rights with {title} as title!**"
        )
    except Exception as e:
        await message.edit(f"{e}")
    if title:
        try:
            await app.set_administrator_title(message.chat.id, user, title)
        except:
            pass


@app.on_message(filters.command("demote", PREFIX) & filters.me)
async def demote(client, message: Message):
    if await CheckAdmin(message) is False:
        await message.edit("**I am not admin.**")
        return
    reply = message.reply_to_message
    if reply:
        user = reply.from_user.id
    else:
        user = get_arg(message)
        if not user:
            await message.edit("**I can't demote no-one, can I?**")
            return
    get_user = await app.get_users(user)
    try:
        await app.promote_chat_member(
            message.chat.id,
            user,
            ChatPrivileges(can_manage_chat=False)
        )
        await message.edit(
            f"**{get_user.first_name} is now stripped off of their admin rights!**"
        )
    except Exception as e:
        await message.edit(f"{e}")


@app.on_message(filters.command("invite", PREFIX) & filters.me & ~filters.private)
async def invite(client, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user.id
    else:
        user = get_arg(message)
        if not user:
            await message.edit("**I can't invite no-one, can I?**")
            return
    get_user = await app.get_users(user)
    try:
        await app.add_chat_members(message.chat.id, get_user.id)
        await message.edit(f"**Added {get_user.first_name} to the chat!**")
    except Exception as e:
        await message.edit(f"{e}")
