# ReBAC Drive - High Stability (No-Docker)

This project has been optimized to run **directly on your Mac** for maximum stability, bypassing all Docker networking and browser security (PNA) issues.

## 🚀 One-Click Start
To start both OpenFGA and the Backend:
```bash
./start_local.sh
```

## ⏹ Stop Services
To stop all background processes:
```bash
./stop_local.sh
```

## 🛠 Service URLs
- **FGA Store Manager (Best UI)**: [http://localhost:8000/](http://localhost:8000/)
  - *Use this to list and create stores without any browser security blocks.*
- **OpenFGA API**: [http://localhost:8080/](http://localhost:8080/)
- **Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Why No-Docker?
1.  **Zero Network Lag**: No virtual bridge between Docker and Mac.
2.  **No Port Conflicts**: Direct access to host ports.
3.  **No PNA Blocks**: Because the UI and API are on the same machine (host), browsers are more lenient with local communication.
4.  **Memory Mode**: OpenFGA is running with a memory-backed datastore for instant performance and no database maintenance required for development.
