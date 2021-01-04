from pyrogram import filters

from Zect import app, CMD_HELP
from Zect.helpers.pyrohelper import get_arg
import Zect.database.notesdb as Zect
from config import PREFIX, LOG_CHAT

CMD_HELP.update({"Notes": """
『 **Notes** 』
  `save` -> Save a new note. Must be used in reply with one parameter (note name).
  `get` -> Gets the note specified.
  `clear` -> Deletes a note, specified by note name.
  `clearall` -> Deletes all the saved notes.
  `notes` -> List the saved notes.
"""})

LOG_CHAT = LOG_CHAT


@app.on_message(filters.command("save", PREFIX) & filters.me)
async def save(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**You must give a name for a note.**")
        return
    note_name = arg
    note = Zect.get_note(note_name)
    if note:
        await message.edit(f"**Note `{note_name}` already exists**")
        return
    reply = message.reply_to_message
    if not reply:
        await message.edit("Reply to a message to save a note")
        return
    copy = await app.copy_message(LOG_CHAT, message.chat.id, reply.message_id)
    Zect.save_note(note_name, copy.message_id)
    await message.edit("**Note saved**")


@app.on_message(filters.command("get", PREFIX) & filters.me)
async def get(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("Get what?")
        return
    note_name = arg
    note = Zect.get_note(note_name)
    if not note:
        await message.edit(f"**Note {note_name} dosen't exists**")
        return
    await app.copy_message(message.chat.id, LOG_CHAT, note)
    await message.delete()


@app.on_message(filters.command("clear", PREFIX) & filters.me)
async def clear(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("What do you want to delete?")
        return
    note_name = arg
    note = Zect.get_note(note_name)
    if not note:
        await message.edit(f"**Failed to delete note `{note_name}`**")
        return
    Zect.rm_note(note_name)
    await message.edit(f"**Succesfully deleted note `{note_name}`**")


@app.on_message(filters.command("notes", PREFIX) & filters.me)
async def notes(client, message):
    msg = "**Saved Notes**\n\n"
    all_notes = Zect.all_notes()
    if not all_notes:
        await message.edit("**No notes has been saved**")
        return
    for notes in all_notes:
        msg += f"> `{notes}`\n"
    await message.edit(msg)


@app.on_message(filters.command("clearall", PREFIX) & filters.me)
async def clearall(client, message):
    Zect.rm_all()
    await message.edit("**Removed all saved notes**")
