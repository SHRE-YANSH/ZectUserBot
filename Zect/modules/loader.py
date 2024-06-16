from config import PREFIX
from pyrogram import filters
from Zect import app, CMD_HELP, HELP
from Zect.database import loaderdb
from Zect.modules.paste import paste
from Zect.helpers.pyrohelper import load_module
from Zect.helpers.pyrohelper import get_arg
from urllib.parse import urlparse

CMD_HELP.update(
    {
        "Loader": """
『 **Loader** 』
  `install` -> Install a module. eg .install raw_url / .install reply to a py file
"""
    }
)

@app.on_message(filters.command("install", PREFIX) & filters.me)
async def install(client, message):
    edit_text = await message.edit("`Installing..`")
    url = get_arg(message)
    if url:
        parsed_url = urlparse(url)
        if not (parsed_url.scheme and parsed_url.netloc and "raw" in parsed_url.path):
            await edit_text.edit("Invalid URL format. Please provide a valid URL with scheme (http/https) and domain.")
    elif not message.reply_to_message:
        await message.edit("`Reply to a py file`")
        return
    elif message.reply_to_message.text:
        await message.edit("`Reply to a py file`")
        return
    else:
        if not message.reply_to_message.document.file_name.endswith(".py"):
            await message.edit("`Reply to a py file`")
            return
        file = await app.download_media(message.reply_to_message.document.file_id)
        with open(file, "r") as f:
            text = f.read()
            f.close()
    status_message = await message.edit("`Installing ...`")
    try:
        raw_url = f'https://spaceb.in/api/v1/documents/{paste(text)}/raw'
    except Exception as e:
        print(e)
        await status_message.delete()
        return
    await load_module(raw_url)
    await status_message.edit("`Installed Successfully`")
    return
