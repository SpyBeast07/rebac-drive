# ReBAC Drive

## Running the Application Locally
To start all services:
```bash
docker compose up -d
```

## Service URLs
- **FGA Store Manager (Recommended)**: [http://localhost:8000/](http://localhost:8000/)
  - *Use this to list and create stores without any browser security issues.*
- **OpenFGA API**: [http://localhost:8080/](http://localhost:8080/)
- **FastAPI Health Check**: [http://localhost:8000/health](http://localhost:8000/health)
- **Official Playground**: [http://localhost:3000/playground](http://localhost:3000/playground)
  - *Note: Requires disabling the `Block insecure private network requests` flag in Chrome.*

## 🛠 Features
- **Native Store Manager**: A custom UI built into the backend to bypass PNA/CORS blocks.
- **Automatic Migrations**: Database schema is initialized automatically on startup.
- **Health-Aware Startup**: Services wait for PostgreSQL to be healthy before starting.
