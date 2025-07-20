# backend/firebase_config.py

import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials

# Load .env file
load_dotenv()

def initialize_firebase():
    if not firebase_admin._apps:
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        db_url = os.getenv("FIREBASE_DATABASE_URL")  # For Realtime DB

        if not cred_path:
            raise ValueError("Missing GOOGLE_APPLICATION_CREDENTIALS in .env")

        cred = credentials.Certificate(cred_path)

        # If Realtime DB URL is set, initialize with databaseURL
        if db_url:
            firebase_admin.initialize_app(cred, {
                'databaseURL': db_url
            })
        else:
            firebase_admin.initialize_app(cred)
