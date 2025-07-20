from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from services.item_service import RealtimeItemService
from schemas import ItemCreate, ItemOut
from services.transaction_service import SwapTransactionService
import cloudinary
import cloudinary.uploader
import asyncio
import os
import json

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
item_service = RealtimeItemService()
swap_service = SwapTransactionService()

# -------------------------
# BASIC CRUD
# -------------------------

@app.post("/items/", response_model=Dict[str, str])
def create_item(item: ItemCreate):
    item_data = item.dict()
    item_id = item_service.create_item(item_data)
    return {"id": item_id}

@app.get("/items/{item_id}", response_model=ItemOut)
def read_item(item_id: str):
    item = item_service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item["id"] = item_id
    return item

@app.get("/items/", response_model=List[ItemOut])
def read_all_items():
    return item_service.get_all_items()

@app.put("/items/{item_id}")
def update_item(item_id: str, updates: Dict):
    existing = item_service.get_item(item_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Item not found")
    item_service.update_item(item_id, updates)
    return {"message": "Item updated"}

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    existing = item_service.get_item(item_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Item not found")
    item_service.delete_item(item_id)
    return {"message": "Item deleted"}

# -------------------------
# SWAP
# -------------------------

@app.post("/swap/{item_id_1}/{item_id_2}")
def swap_items(item_id_1: str, item_id_2: str):
    try:
        swap_service.swap_items(item_id_1, item_id_2)
        return {"message": f"Items {item_id_1} and {item_id_2} swapped successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# -------------------------
# IMAGE UPLOAD + RETURN URL
# -------------------------

@app.post("/upload-images")
async def upload_images(
    files: List[UploadFile] = File(...),
    tags: str = Form("rewear"),
    context: str = Form("Item Number")
):
    tag_list = [tag.strip() for tag in tags.split(",")]
    results = []

    for file in files:
        upload_result = await asyncio.to_thread(
            cloudinary.uploader.upload,
            file.file,
            public_id=file.filename.rsplit(".", 1)[0],
            folder="rewear-items",
            tags=tag_list,
            context={"caption": context}
        )
        results.append({
            "filename": file.filename,
            "cloudinary_url": upload_result["secure_url"],
            "public_id": upload_result["public_id"],
            "tags": tag_list,
            "context": upload_result.get("context", {}).get("custom", {})
        })

    return {"uploaded_images": results}

# -------------------------
# CREATE ITEM + IMAGE UPLOAD IN ONE
# -------------------------

@app.post("/items/create-with-images", response_model=Dict[str, str])
async def create_item_with_images(
    item_data: str = Form(...),
    files: List[UploadFile] = File(...)
):
    try:
        parsed_item = json.loads(item_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid item JSON: {str(e)}")

    # Upload images
    image_urls = []
    for file in files:
        upload_result = await asyncio.to_thread(
            cloudinary.uploader.upload,
            file.file,
            public_id=file.filename.rsplit(".", 1)[0],
            folder="rewear-items"
        )
        image_urls.append(upload_result["secure_url"])

    parsed_item["image_urls"] = image_urls
    item_id = item_service.create_item(parsed_item)
    return {"id": item_id}
