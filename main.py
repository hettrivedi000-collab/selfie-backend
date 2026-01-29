from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from database import db
from database import collection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UploadPayload(BaseModel):
    name: str
    mobile: str
    occupation: str
    city: str
async def get_next_serial():
    counter = await db.collection.find_one_and_update(
        {"_id":"COUNTER"},
        {"$inc":{"seq":1}},
        upsert=true,
        return_document=true
    )
    return counter["seq"]

@app.post("/upload")
async def upload_user(payload: UploadPayload):
    next_serial=await get_next_serial()     

    doc = {
        "serial_no": next_serial,
        "name": payload.name,
        "mobile": payload.mobile,
        "occupation": payload.occupation,
        "city": payload.city,
        "created_at": datetime.utcnow()
    }

    await collection.insert_one(doc)

    return {
        "success": True
    }


@app.get("/all-users")
async def get_all_users():
    users = []
    cursor = collection.find({"_id":{"$ne":"COUNTER"}).sort("serial_no",-1)

    async for u in cursor:
        users.append({
            "serial_no": u["serial_no"],
            "name": u["name"],
            "mobile": u["mobile"],
            "occupation": u["occupation"],
            "city": u["city"],
            "created_at": u["created_at"]
        })

    return users



