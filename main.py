from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

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


@app.post("/upload")
async def upload_user(payload: UploadPayload):
    last = await collection.find_one(sort=[("serial_no", -1)])
    next_serial = 1 if last is None else last["serial_no"] + 1

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
    cursor = collection.find().sort("serial_no", -1)

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
