import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import dotenv
dotenv.load_dotenv()
import os
import json

# print(os.getenv("GDrive_SERVICE_ACCOUNT_INFO"))

SERVICE_ACCOUNT_INFO = json.loads(os.getenv("GDrive_SERVICE_ACCOUNT_INFO"))

# Path to your Service Account Key JSON file
cred = credentials.Certificate(SERVICE_ACCOUNT_INFO)

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv("databaseURL")  # Replace with your database URL
})

# Initialize Firestore DB
db = firestore.client()