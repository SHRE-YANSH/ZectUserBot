from pymongo import MongoClient
from config import MONGO_URI

cli = MongoClient(MONGO_URI)
