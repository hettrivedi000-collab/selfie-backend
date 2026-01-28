from motor.motor_asyncio import AsyncIOMotorClient
import os
MONGO_URL = os.getenv("MANGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
db = client["selfie_db"]
collection = db["users"]


