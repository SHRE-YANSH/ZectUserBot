from . import cli

collection = cli["Zect"]["gmute"]


def gmute_user(chat: int):
    doc = {"_id": chat, "gmute": True}
    r = collection.find_one({"_id": chat})
    if r:
        collection.update_one({"_id": chat}, {"$set": {"gmute": True}})
    else:
        collection.insert_one(doc)


def get_gmuted_users():
    chats = []
    results = collection.find({"gmute": True})
    for result in results:
        chats.append(result["_id"])
    return chats


def ungmute_user(chat):
    collection.update_one({"_id": chat}, {"$set": {"gmute": False}})
