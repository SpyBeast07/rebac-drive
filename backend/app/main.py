import os
import threading
import httpx
from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from openfga_sdk import OpenFgaClient, ClientConfiguration
from openfga_sdk.client.models import ClientCheckRequest, ClientWriteRequest
from fastapi.middleware.cors import CORSMiddleware
from .models import Base, File, Folder
from .scanner import start_scanner

import shutil
from .scanner import Scanner

# Configuration
STORE_ID = "01KMQQEE506DVHNYFQVTYWPPKQ"
FGA_API_URL = "http://localhost:8080"
DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"

# Global state
class GlobalState:
    storage_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../storage"))
    scanner = None

state = GlobalState()

# DB Setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FGA Setup
fga_config = ClientConfiguration(
    api_url=FGA_API_URL,
    store_id=STORE_ID
)
fga_client = OpenFgaClient(fga_config)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    state.scanner = Scanner(state.storage_path, DATABASE_URL)
    threading.Thread(target=state.scanner.start, daemon=True).start()

@app.get("/system/storage-info")
async def get_storage_info():
    total, used, free = shutil.disk_usage(state.storage_path)
    return {
        "total": total,
        "used": used,
        "free": free,
        "path": state.storage_path
    }

@app.post("/settings/storage-path")
async def update_storage_path(path: str = Form(...), db: Session = Depends(get_db)):
    if not os.path.exists(path):
        raise HTTPException(status_code=400, detail="Path does not exist")
    
    # 1. Stop old scanner
    if state.scanner:
        state.scanner.stop()
    
    # 2. Update path
    state.storage_path = os.path.abspath(path)
    
    # 3. Clear DB (optional but recommended for clean swap)
    db.query(File).delete()
    db.query(Folder).delete()
    db.commit()
    
    # 4. Start new scanner
    state.scanner = Scanner(state.storage_path, DATABASE_URL)
    threading.Thread(target=state.scanner.start, daemon=True).start()
    
    return {"status": "updated", "path": state.storage_path}

@app.get("/files/{file_id}")
async def get_file(file_id: str, user_id: str, db: Session = Depends(get_db)):
    # ... (existing logic) ...
    response = await fga_client.check(ClientCheckRequest(
        user=f"user:{user_id}",
        relation="viewer",
        object=f"file:{file_id}"
    ))
    if not response.allowed: raise HTTPException(status_code=403, detail="Access denied")
    return db.query(File).filter(File.id == file_id).first()

@app.get("/folders/root")
async def get_root_folder(user_id: str, db: Session = Depends(get_db)):
    # Root folders: parent_id=None
    folders = db.query(Folder).filter(Folder.parent_id == None).all()
    # ALL files at the root level (no limit)
    files = db.query(File).filter(File.parent_id == None).all()
    return {"folders": folders, "files": files}

@app.get("/files/{file_id}/content")
async def get_file_content(file_id: str, user_id: str, db: Session = Depends(get_db)):
    response = await fga_client.check(ClientCheckRequest(
        user=f"user:{user_id}",
        relation="viewer",
        object=f"file:{file_id}"
    ))
    if not response.allowed: raise HTTPException(status_code=403, detail="Access denied")
    file_entry = db.query(File).filter(File.id == file_id).first()
    if not file_entry: raise HTTPException(status_code=404, detail="File not found")
    file_path = os.path.join(state.storage_path, file_entry.path)
    return FileResponse(file_path)

@app.get("/folders/{folder_id}")
async def get_folder(folder_id: str, user_id: str, db: Session = Depends(get_db)):
    response = await fga_client.check(ClientCheckRequest(
        user=f"user:{user_id}",
        relation="viewer",
        object=f"folder:{folder_id}"
    ))
    if not response.allowed: raise HTTPException(status_code=403, detail="Access denied")
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    return {"folder": folder, "folders": folder.children, "files": folder.files}

@app.get("/health")
def health():
    return {"status": "ok", "storage": state.storage_path}
