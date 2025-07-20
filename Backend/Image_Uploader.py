import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from pathlib import Path

import dotenv
import os
dotenv.load_dotenv()

print("Environment variables loaded successfully.")


# Configuration       
cloudinary.config( 
    cloud_name = os.getenv("Cloudinary_Cloud_name"), 
    api_key = os.getenv("Cloudinary_API_key"), 
    api_secret = os.getenv("Cloudinary_API_secret"), # Click 'View API Keys' above to copy your API secret
    secure=True
)

def Image_Upload(image_path):
    print("called")
    path = str(Path(image_path))

    print("Uploading image from path:", path)
    
    upload_result = cloudinary.uploader.upload(
        path,
        public_id="shoes",
        folder="rewear-items",
        tags=["rewear", "tshirt", "men"],
        context={"alt": "Casual summer shoes", "caption": "Brown casual shoes"}
        )   

    print("Image URL:", upload_result["secure_url"])

    # Optimize delivery by resizing and applying auto-format and auto-quality
    optimize_url, _ = cloudinary_url("shoes", fetch_format="auto", quality="auto")

    auto_crop_url, _ = cloudinary_url("shoes", width=500, height=500, crop="auto", gravity="auto")



Image_Upload("C:\Users\satwi\Downloads\Pi7_Passport_Photo.jpeg")