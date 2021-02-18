import motor.motor_asyncio
from config import MONGO_URI


cli = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
