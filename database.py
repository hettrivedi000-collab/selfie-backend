from motor.motor_asyncio import AsyncIOMotorClient
import os
MONGO_URI = os.getenv("MANGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["selfie_db"]
collection = db["users"]

