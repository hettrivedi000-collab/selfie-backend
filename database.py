from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://hettrivedi:Het%40123@waha.ysyutuo.mongodb.net/selfie_db?retryWrites=true&w=majority"
collection="users"
client = AsyncIOMotorClient(MONGO_URI)
db = client["selfie_db"]
collection = db["users"]
