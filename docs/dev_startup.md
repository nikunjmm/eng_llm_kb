# Developer Startup Guide

This guide covers everything you need to start the foundational services of the Agentic RAG Framework locally.

## Prerequisites
*   [Docker](https://docs.docker.com/get-docker/) & Docker Compose
*   [Python 3.10+](https://www.python.org/downloads/)
*   [Node.js (v18+)](https://nodejs.org/)
*   Git

## 1. Start Local Infrastructure Services

Our data layer is fully containerized using Docker. This includes our unified database (`pgvector`), image storage (`MinIO`), and our LLM observability platform (`Langfuse`).

Navigate to the `docker` directory and start the services:

```bash
cd docker
docker compose up -d
```

### Checking Services
Once the containers are built and running, you can access:
*   **PostgreSQL (pgvector)**: Listening on `localhost:5433` 
*   **MinIO Console**: [http://localhost:9001](http://localhost:9001) (Credentials: `admin` / `password123`)
*   **Langfuse Dashboard**: [http://localhost:3000](http://localhost:3000)

---

## 2. API & Orchestration Server (Python)

The backend runs on Python via FastAPI. You will need to install the dependencies (like `pydantic`, `fastapi`, `docling`, `psycopg2`, etc.).

*Note: The exact requirements format will be established during the Python backend implementation phase, but typically involves creating a virtual environment and installing packages.*

```bash
# Example setup (adjust pathing pending final project structure)
cd backend 
python -m venv venv

# Activate venv (Windows)
.\venv\Scripts\activate
# Activate venv (Linux/Mac)
source venv/bin/activate

pip install -r requirements.txt

# Start the development server (uvicorn)
uvicorn main:app --reload --port 8000
```
This will start the FastAPI backend swagger docs at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 3. Client UI Application (React / TypeScript)

The UI component is designed to be embedded in a C# WebView2 wrapper but operates as a standard React app during development.

*Note: The exact structural commands will depend on your package manager (npm, yarn, pnpm) established during the UI initialization phase.*

```bash
# Example setup (adjust pathing pending final project structure)
cd client-ui
npm install

# Start the dev server
npm run dev
```

The UI should now be accessible locally, typically at [http://localhost:5173](http://localhost:5173) (if using Vite) or `3000`.

---

## Stopping the Infrastructure 

To spin down the Docker containers without clearing your data:
```bash
cd docker
docker compose stop
```

To entirely remove the containers:
```bash
cd docker
docker compose down
```
