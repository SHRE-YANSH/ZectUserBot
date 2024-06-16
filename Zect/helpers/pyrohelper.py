# Copyright (C) 2020-2021 by shre-yansh@Github, < https://github.com/shre-yansh >.
#
# This file is part of < https://github.com/shre-yansh/ZectUserBot > project,
# and is released under the "AGP v3.0 License Agreement".
# Please see < https://github.com/shre-yansh/ZectUserBot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram.types import Message, User
from pyrogram import Client
from Zect.database.afkdb import get_afk_status
from Zect.database.pmpermitdb import get_approved_users, pm_guard
import Zect.database.welcomedb as Zectdb
from Zect.database import loaderdb
import shlex
import logging
import tempfile
import importlib
import requests
from urllib.parse import urlparse

def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


def get_args(message):
    try:
        message = message.text
    except AttributeError:
        pass
    if not message:
        return False
    message = message.split(maxsplit=1)
    if len(message) <= 1:
        return []
    message = message[1]
    try:
        split = shlex.split(message)
    except ValueError:
        return message  # Cannot split, let's assume that it's just one long message
    return list(filter(lambda x: len(x) > 0, split))


async def user_afk(filter, client: Client, message: Message):
    check = await get_afk_status()
    if check:
        return True
    else:
        return False


async def denied_users(filter, client: Client, message: Message):
    if not await pm_guard():
        return False
    if message.chat.id in (await get_approved_users()):
        return False
    else:
        return True


async def welcome_chat(filter, client: Client, message: Message):
    to_welcome = await Zectdb.get_welcome(str(message.chat.id))
    if to_welcome:
        return True
    else:
        return False
    
async def load_module(uri=None):
    module_name = None
    required_packages = []
    modules = await loaderdb.all_modules()
    if not uri and not modules:
        logging.info(f"No external modules found.")
        return
    elif modules:
        raw_url = [module["raw_url"] for module in modules]
    else:
        raw_url = [uri]
    for url in raw_url:
        parsed_url = urlparse(url)
        if not (parsed_url.scheme and parsed_url.netloc):
            raise ValueError("Invalid URL format. Please provide a valid URL with scheme (http/https) and domain.")

        # Download the module code using requests
        try:
            response = requests.get(url)
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to download module: {e}")

        # Create a temporary file to store the downloaded code
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(response.content)   
            temp_file.seek(0)  # Move the file pointer to the beginning of the file

            with open(temp_file.name, 'r') as f:
                for line in f:
                    if line.startswith("# name = "):
                        module_name = line.strip().split("=")[1].strip()
                    if line.startswith("# require = "):
                        package_list = line.strip().split("=")[1].strip()
                        required_packages.extend(package.strip() for package in package_list.split(","))
                        break
        if not module_name:
            raise ValueError("Module is missing required comment '# name = module_name'")
        # Install required packages if present
        if required_packages:
            import pip
            try:
                for package in required_packages:
                    pip.main(['install', package])
            except Exception as e:
                print(f"Failed to install required packages: {e}")


        try:
            spec = importlib.util.spec_from_file_location(module_name, temp_file.name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            logging.info(f"Module {module_name} loaded successfully.")
            if uri:
                await loaderdb.save_module(module_name, url)
            return module
        except Exception as e:
            raise ImportError(f"Failed to import module: {e}")
        finally:
            # Regardless of success or failure, remove the temporary file
            import os
            os.remove(temp_file.name)

