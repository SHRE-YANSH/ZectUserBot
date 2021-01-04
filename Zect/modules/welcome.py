from pyrogram import filters

from Zect import app, CMD_HELP
from Zect.helpers.pyrohelper import get_arg
import Zect.database.welcomedb as Zectdb
from config import PREFIX, LOG_CHAT

CMD_HELP.update({"Greetings": """
『 **Greetings** 』
  `welcome` [on or off] -> Activates or deactivates welcome.
  `setwelcome` -> Sets a custom welcome message.
  """})

LOG_CHAT = LOG_CHAT


@app.on_message(filters.chat(Zectdb.get_welcome_chat()) & filters.new_chat_members)
async def send_welcome(client, message):
    media, content = Zectdb.get_welcome(message.chat.id)
    if media:
        msg = await app.get_messages(LOG_CHAT, content)
        if msg.caption:
            caption = msg.caption
            if '{mention}' in caption:
                men = caption.replace("{mention}", "[{}](tg://user?id={})")
        if msg.photo and caption is not None:
            await app.send_photo(message.chat.id, msg.photo.file_id, caption=men.format(message.new_chat_members[0]["first_name"], message.new_chat_members[0]["id"]), reply_to_message_id=message.message_id)
        if msg.animation and caption is not None:
            await app.send_animation(message.chat.id, msg.animation.file_id, caption=men.format(message.new_chat_members[0]["first_name"], message.new_chat_members[0]["id"]), reply_to_message_id=message.message_id)
        if msg.sticker:
            await app.send_sticker(message.chat.id, msg.sticker.file_id, reply_to_message_id=message.message_id)

    else:
        if '{mention}' in content:
            men = content.replace("{mention}", "[{}](tg://user?id={})")
            await app.send_message(message.chat.id, men.format(message.new_chat_members[0]["first_name"], message.new_chat_members[0]["id"]), reply_to_message_id=message.message_id)
        else:
            await app.send_message(message.chat.id, content, reply_to_message_id=message.message_id)


@app.on_message(filters.command("welcome", PREFIX) & filters.me)
async def welcome(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**I only understand on or off**")
        return
    if arg == "off":
        Zectdb.welcome(message.chat.id, False)
        await message.edit("**I am sulking not to say hello anymore :(**")
    if arg == "on":
        Zectdb.welcome(message.chat.id, True)
        await message.edit("**I'll be polite**")


@app.on_message(filters.command("setwelcome", PREFIX) & filters.me)
async def setwelcome(client, message):
    Zectdb.welcome(message.chat.id, True)
    reply = message.reply_to_message
    welcome_msg = None
    media_id = None
    if reply:
        if reply.text:
            welcome_msg = reply.text
        if reply.media:
            frwd = await app.copy_message(LOG_CHAT, message.chat.id, reply.message_id)
            media_id = frwd.message_id
            caption = frwd.caption
    else:
        welcome_msg = get_arg(message)
    if welcome_msg or media_id is None:
        await message.edit("**You didn't specify what to reply with.**")
        return
    Zectdb.set_welcome(message.chat.id, welcome_msg, media_id)
    await message.edit("**Welcome message has been saved.**")
