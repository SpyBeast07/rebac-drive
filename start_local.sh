#!/bin/bash

# 1. Kill any existing processes
echo "Cleaning up existing processes..."
pkill openfga
pkill uvicorn

# 2. Start OpenFGA in memory mode (extremely stable, no DB needed for dev)
echo "Starting OpenFGA (Local Binary)..."
./openfga run --datastore-engine memory > openfga.log 2>&1 &
echo "OpenFGA started in background."

# 3. Start Backend
echo "Starting FastAPI Backend..."
cd backend
pip install -r requirements.txt > /dev/null 2>&1
uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
echo "Backend started in background."

echo "------------------------------------------------"
echo "Services are ready!"
echo "Dashboard: http://localhost:8000/ (Primary Store Management)"
echo "API Server: http://localhost:8080/"
echo "Official UI: http://localhost:3000/playground (Note: requires browser flag fix)"
echo "------------------------------------------------"
echo "To stop services: pkill openfga && pkill uvicorn"
