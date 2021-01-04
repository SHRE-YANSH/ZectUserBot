from . import cli

collection = cli["Zect"]["afk"]

doc = {"_id": 1, "afk_status": False}
r = collection.find_one({"_id": 1})
if r:
    pass
else:
    collection.insert_one(doc)


def set_afk(afk_status, afk_since, reason):
    collection.update_one(
        {"_id": 1},
        {"$set": {"afk_status": afk_status, "afk_since": afk_since, "reason": reason}},
    )


def set_unafk():
    collection.update_one(
        {"_id": 1}, {"$set": {"afk_status": False, "afk_since": None, "reason": None}}
    )


def get_afk_status():
    result = collection.find_one({"_id": 1})
    status = result["afk_status"]
    return status


def afk_stuff():
    result = collection.find_one({"_id": 1})
    afk_since = result["afk_since"]
    reason = result["reason"]
    return afk_since, reason
