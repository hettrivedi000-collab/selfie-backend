import os
import base64
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
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

os.makedirs("selfies", exist_ok=True)

class UploadPayload(BaseModel):
    name: str
    mobile: str
    image: str


@app.post("/upload")
async def upload_selfie(payload: UploadPayload):
    last = await collection.find_one(sort=[("serial_no", -1)])
    next_serial = 1 if last is None else last["serial_no"] + 1

    header, encoded = payload.image.split(",", 1)
    image_bytes = base64.b64decode(encoded)

    img = Image.open(BytesIO(image_bytes)).convert("RGB")

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{payload.mobile}_{timestamp}.jpg"
    filepath = os.path.join("selfies", filename)

    img.save(filepath, format="JPEG", quality=95)

    doc = {
        "serial_no": next_serial,
        "name": payload.name,
        "mobile": payload.mobile,
        "image_path": filepath,
        "created_at": datetime.utcnow()
    }

    await collection.insert_one(doc)

    return {
        "success": True,
        "serial_no": next_serial
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
            "image_path": u["image_path"],
            "created_at": u["created_at"]
        })

    return users
