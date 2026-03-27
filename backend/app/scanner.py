import os
import time
import logging
import httpx
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sqlalchemy.orm import Session
from .models import File, Folder, Base
from sqlalchemy import create_engine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STORE_ID = "01KMQQEE506DVHNYFQVTYWPPKQ"

def write_fga_tuples(tuples):
    if not tuples: return
    try:
        # FGA supports up to 10 tuples per write
        for i in range(0, len(tuples), 10):
            batch = tuples[i:i+10]
            resp = httpx.post(f"http://localhost:8080/stores/{STORE_ID}/write", json={
                "writes": { "tuple_keys": batch }
            })
            if resp.status_code == 200:
                logger.info(f"FGA Batch Written: {len(batch)} tuples")
            else:
                logger.error(f"FGA Batch Failed: {resp.text}")
    except Exception as e:
        logger.error(f"Error writing to FGA: {e}")

class FileScannerHandler(FileSystemEventHandler):
    def __init__(self, db_session: Session, storage_path: str):
        self.db = db_session
        self.storage_path = os.path.abspath(storage_path)

    def on_created(self, event):
        self.sync_item(event.src_path)

    def on_moved(self, event):
        self.sync_item(event.dest_path)

    def sync_item(self, full_path):
        rel_path = os.path.relpath(full_path, self.storage_path)
        if os.path.isdir(full_path):
            _get_or_create_folder(self.db, rel_path, self.storage_path)
        else:
            _get_or_create_file(self.db, rel_path, self.storage_path)

def scan_initial(db: Session, storage_path: str):
    logger.info("Performing initial scan...")
    storage_path = os.path.abspath(storage_path)
    
    # We'll collect FGA tuples and write them in batches
    fga_tuples = []

    for root, dirs, files in os.walk(storage_path):
        for d in dirs:
            full_path = os.path.join(root, d)
            rel_path = os.path.relpath(full_path, storage_path)
            folder, new = _get_or_create_folder_internal(db, rel_path, storage_path)
            if new:
                # Assign owner
                fga_tuples.append({ "user": "user:user1", "relation": "owner", "object": f"folder:{folder.id}" })
                # Assign parent for inheritance
                if folder.parent_id:
                    fga_tuples.append({ "user": f"folder:{folder.parent_id}", "relation": "parent", "object": f"folder:{folder.id}" })
            
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, storage_path)
            file_entry, new = _get_or_create_file_internal(db, rel_path, storage_path)
            if new:
                fga_tuples.append({ "user": "user:user1", "relation": "owner", "object": f"file:{file_entry.id}" })
                if file_entry.parent_id:
                    fga_tuples.append({ "user": f"folder:{file_entry.parent_id}", "relation": "parent", "object": f"file:{file_entry.id}" })

        # Flush batches every directory to keep memory low
        if len(fga_tuples) > 50:
            write_fga_tuples(fga_tuples)
            fga_tuples = []

    write_fga_tuples(fga_tuples)

def _get_or_create_folder_internal(db, rel_path, storage_path):
    if rel_path == "." or not rel_path: return None, False
    folder = db.query(Folder).filter(Folder.path == rel_path).first()
    new = False
    if not folder:
        name = os.path.basename(rel_path)
        parent_path = os.path.dirname(rel_path)
        parent, _ = _get_or_create_folder_internal(db, parent_path, storage_path)
        folder = Folder(name=name, path=rel_path, parent_id=parent.id if parent else None)
        db.add(folder)
        db.commit()
        db.refresh(folder)
        new = True
        logger.info(f"Indexed Folder: {rel_path}")
    return folder, new

def _get_or_create_file_internal(db, rel_path, storage_path):
    file_entry = db.query(File).filter(File.path == rel_path).first()
    new = False
    if not file_entry:
        name = os.path.basename(rel_path)
        parent_path = os.path.dirname(rel_path)
        parent, _ = _get_or_create_folder_internal(db, parent_path, storage_path)
        file_entry = File(
            name=name, 
            path=rel_path, 
            type=os.path.splitext(name)[1], 
            parent_id=parent.id if parent else None
        )
        db.add(file_entry)
        db.commit()
        db.refresh(file_entry)
        new = True
        logger.info(f"Indexed File: {rel_path}")
    return file_entry, new

def _get_or_create_folder(db, rel_path, storage_path):
    folder, new = _get_or_create_folder_internal(db, rel_path, storage_path)
    if new:
        fga_tuples = [{ "user": "user:user1", "relation": "owner", "object": f"folder:{folder.id}" }]
        if folder.parent_id:
            fga_tuples.append({ "user": f"folder:{folder.parent_id}", "relation": "parent", "object": f"folder:{folder.id}" })
        write_fga_tuples(fga_tuples)
    return folder

def _get_or_create_file(db, rel_path, storage_path):
    file_entry, new = _get_or_create_file_internal(db, rel_path, storage_path)
    if new:
        fga_tuples = [{ "user": "user:user1", "relation": "owner", "object": f"file:{file_entry.id}" }]
        if file_entry.parent_id:
            fga_tuples.append({ "user": f"folder:{file_entry.parent_id}", "relation": "parent", "object": f"file:{file_entry.id}" })
        write_fga_tuples(fga_tuples)
    return file_entry

class Scanner:
    def __init__(self, storage_path: str, db_url: str):
        self.storage_path = os.path.abspath(storage_path)
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.observer = None
        self.running = False

    def start(self):
        logger.info(f"Starting scanner for: {self.storage_path}")
        Base.metadata.create_all(bind=self.engine)
        
        with Session(self.engine) as db:
            scan_initial(db, self.storage_path)
            
            event_handler = FileScannerHandler(db, self.storage_path)
            self.observer = Observer()
            self.observer.schedule(event_handler, self.storage_path, recursive=True)
            self.observer.start()
            self.running = True
            logger.info(f"Observer active on {self.storage_path}")

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.running = False
            logger.info("Scanner stopped")

# Compatibility wrapper for old calls
def start_scanner(storage_path: str, db_url: str):
    scanner = Scanner(storage_path, db_url)
    scanner.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scanner.stop()
