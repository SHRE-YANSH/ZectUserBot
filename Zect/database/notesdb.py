from pyrogram.filters import chat
from .import cli

collection = cli["Zect"]["notes"]


def save_note(note_name, note_id):
    doc = {"_id": 1, "notes": {note_name: note_id}}
    result = collection.find_one({"_id": 1})
    if result:
        collection.update_one(
            {"_id": 1}, {"$set": {f"notes.{note_name}": note_id}})
    else:
        collection.insert_one(doc)


def get_note(note_name):
    result = collection.find_one({"_id": 1})
    if result is not None:
        try:
            note_id = result["notes"][note_name]
            return note_id
        except KeyError:
            return None
    else:
        return None


def rm_note(note_name):
    collection.update_one(
        {"_id": 1}, {"$unset": {f"notes.{note_name}": ""}})


def all_notes():
    all_notes = []
    results = collection.find_one({"_id": 1})
    try:
        notes_dic = results["notes"]
        key_list = notes_dic.keys()
        return key_list
    except:
        return None


def rm_all():
    collection.update_one(
        {"_id": 1}, {"$unset": {"notes": ""}})
