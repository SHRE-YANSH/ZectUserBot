from . import cli

collection = cli["Zect"]["gmute"]


def gmute_user(chat):
    doc = {"_id": "Gmute", "users": [chat]}
    r = collection.find_one({"_id": "Gmute"})
    if r:
        collection.update_one({"_id": "Gmute"}, {"$push": {"users": chat}})
    else:
        collection.insert_one(doc)


def get_gmuted_users():
    results = collection.find_one({"_id": "Gmute"})
    if results:
        return results["users"]
    else:
        return []


def ungmute_user(chat):
    collection.update_one({"_id": "Gmute"}, {"$pull": {"users": chat}})
