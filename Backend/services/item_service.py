from services.firebase_config import initialize_firebase
from firebase_admin import db
from datetime import datetime
import cloudinary
import cloudinary.uploader
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

class RealtimeItemService:
    def __init__(self):
        initialize_firebase()
        self.ref = db.reference("items")

    def create_item(self, item_data: dict):
        item_data["created_at"] = datetime.now().isoformat()
        new_ref = self.ref.push()
        new_ref.set(item_data)
        return new_ref.key

    def get_item(self, item_id: str):
        item = self.ref.child(item_id).get()
        if item:
            item["id"] = item_id
        return item

    def update_item(self, item_id: str, updates: dict):
        self.ref.child(item_id).update(updates)

    def delete_item(self, item_id: str):
        self.ref.child(item_id).delete()

    def get_all_items(self):
        data = self.ref.get()
        if isinstance(data, dict):
            return [
                {**value, "id": key}
                for key, value in data.items() if isinstance(value, dict)
            ]
        elif isinstance(data, list):
            return [
                {**value, "id": str(idx)}
                for idx, value in enumerate(data) if isinstance(value, dict)
            ]
        return []

    # ✅ Upload image and return Cloudinary URL
    def upload_images(self, files: List):
        results = []
        for file in files:
            upload_result = cloudinary.uploader.upload(
                file.file,
                public_id=file.filename.rsplit(".", 1)[0],
                folder="rewear-items",
                tags=["rewear"],
                context={"caption": "Item Upload"}
            )
            results.append(upload_result["secure_url"])
        return results
