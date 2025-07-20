from fastapi import FastAPI, Request, Depends, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

import dotenv
import shutil
import os
import threading
import asyncio
import time

dotenv.load_dotenv()

# Create an instance of FastAPI
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/Get_Menu")
async def Menu():
    return "Running"

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    
    async with asyncio.to_thread(open, file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    label = await asyncio.to_thread(detect, file_path)
    
    return {"filename": label}