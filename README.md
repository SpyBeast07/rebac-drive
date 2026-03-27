# ReBAC Drive - Personal Local Explorer 🚀📂

A high-performance, Google Drive-style web interface for your local laptop storage, secured with **OpenFGA** (Relationship-Based Access Control).

## ✨ Key Features
- **Personalized UI**: Streamlined interface focused on local file management.
- **Dynamic Storage Selector**: Point the drive to ANY absolute path on your laptop (e.g., `/Users/me/Downloads`) and watch it re-index instantly.
- **Real-Time Device Stats**: Live reporting of your laptop's actual disk usage.
- **File Previews**: View Text, Images, and PDFs directly in the browser.
- **Optimized Indexing**: High-performance scanner with batch FGA writes and ReBAC inheritance for fast processing of thousands of files.

## 🚀 Getting Started

### 1. Start OpenFGA & Backend
Run the local start script to boot the memory-backed OpenFGA server and the FastAPI backend:
```bash
./start_local.sh
```

### 2. Start Frontend
```bash
cd frontend
npm install
npm run dev -- --port 5174
```

## 🛠 Service Overview
- **Drive UI**: [http://localhost:5174/](http://localhost:5174/)
- **Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **OpenFGA API**: [http://localhost:8080/](http://localhost:8080/)

## Why This Architecture?
1.  **Direct-to-Mac**: Runs natively for zero network lag and bypassed Docker PNA security restrictions.
2.  **ReBAC Security**: Uses OpenFGA to model complex sharing relationships (viewer/owner) inherited through the folder tree.
3.  **High Scalability**: The scanner uses batch processing to handle directories with 5,000+ files in seconds.
