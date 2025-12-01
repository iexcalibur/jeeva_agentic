# Setup Guide

This guide explains how to set up and run the Jeeva Agentic project in different modes.

## Overview

The project supports two deployment modes:

1. **Development Mode** (`make dev`): Uses SQLite database and in-memory caching
   - No Docker required
   - Fast setup for local development
   - Data persists in `chatbot.db` file

2. **Docker Mode** (`make docker-up`): Uses PostgreSQL and Redis
   - Full production-like setup
   - Requires Docker Desktop
   - Uses Docker Compose for orchestration

## Prerequisites

### For Development Mode
- Python 3.11 or 3.12 (Python 3.14 may have compatibility issues)
- Node.js 18+ and npm
- Virtual environment support

### For Docker Mode
- Docker Desktop installed and running
- Python 3.11 or 3.12 (for local development)
- Node.js 18+ and npm (for frontend)

## Quick Start

### Development Mode (SQLite + In-Memory Cache)

1. **Install dependencies:**
   ```bash
   make install
   ```

2. **Set up environment variables:**
   - The Makefile will auto-create a `.env` file if it doesn't exist
   - Update `ANTHROPIC_API_KEY` in `.env` with your actual API key

3. **Start the application:**
   ```bash
   make dev
   ```
   This will:
   - Initialize SQLite database (`chatbot.db`)
   - Start backend on `http://localhost:8000`
   - Start frontend on `http://localhost:3000`

4. **Stop the application:**
   - Press `Ctrl+C` to stop all services gracefully

### Docker Mode (PostgreSQL + Redis)

1. **Ensure Docker Desktop is running**

2. **Start Docker services:**
   ```bash
   make docker-up
   ```
   This will:
   - Start PostgreSQL on `localhost:5432`
   - Start Redis on `localhost:6379`
   - Start backend API on `http://localhost:8000`
   - Initialize database schema automatically

3. **Set environment variables for Docker:**
   - Create or update `.env` file with:
     ```env
     USE_DOCKER=true
     DATABASE_TYPE=postgresql
     CACHE_TYPE=redis
     ANTHROPIC_API_KEY=your_anthropic_api_key_here
     POSTGRES_HOST=localhost
     POSTGRES_PORT=5432
     POSTGRES_USER=chatbot_user
     POSTGRES_PASSWORD=chatbot_pass
     POSTGRES_DB=chatbot_db
     REDIS_HOST=localhost
     REDIS_PORT=6379
     REDIS_DB=0
     ```

4. **Start frontend separately:**
   ```bash
   make dev-frontend
   ```

5. **Stop Docker services:**
   ```bash
   make docker-stop    # Stop but keep containers
   make docker-down    # Stop and remove containers
   ```

## Environment Variables

### Development Mode (.env)
```env
DATABASE_TYPE=sqlite
CACHE_TYPE=memory
SQLITE_DB_PATH=chatbot.db
ANTHROPIC_API_KEY=your_anthropic_api_key_here
LOG_LEVEL=INFO
DEBUG=false
```

### Docker Mode (.env)
```env
USE_DOCKER=true
DATABASE_TYPE=postgresql
CACHE_TYPE=redis
DATABASE_URL=postgresql://chatbot_user:chatbot_pass@localhost:5432/chatbot_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=chatbot_user
POSTGRES_PASSWORD=chatbot_pass
POSTGRES_DB=chatbot_db
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
ANTHROPIC_API_KEY=your_anthropic_api_key_here
LOG_LEVEL=INFO
DEBUG=false
```

## Database Initialization

The database schema is automatically initialized when you run:
- `make dev` (for SQLite)
- `make docker-up` (for PostgreSQL)

To manually initialize:
```bash
make db-init
```

## Frontend Connection

The frontend is configured to connect to the backend at `http://localhost:8000`. 

### Verify Connection

1. **Check backend health:**
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status":"healthy"}`

2. **Check frontend:**
   - Open `http://localhost:3000` in your browser
   - The frontend should automatically connect to the backend

3. **Test API endpoint:**
   ```bash
   curl http://localhost:8000/api/chat \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"user_id": "test-user", "message": "Hello"}'
   ```

## Troubleshooting

### Backend not connecting to database

**Development Mode (SQLite):**
- Check that `chatbot.db` file exists in the project root
- Run `make db-init` to recreate the database

**Docker Mode (PostgreSQL):**
- Ensure Docker Desktop is running
- Check PostgreSQL container: `docker ps | grep postgres`
- Check logs: `docker-compose logs postgres`
- Verify connection: `docker-compose exec postgres psql -U chatbot_user -d chatbot_db`

### Frontend not connecting to backend

1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check CORS settings:**
   - Backend allows all origins in development
   - Verify frontend is making requests to `http://localhost:8000`

3. **Check browser console:**
   - Open browser DevTools (F12)
   - Look for network errors or CORS issues

### Redis connection issues (Docker mode)

- Check Redis container: `docker ps | grep redis`
- Test Redis: `docker-compose exec redis redis-cli ping`
- Should return: `PONG`

### Database migration issues

- For SQLite: Delete `chatbot.db` and run `make db-init`
- For PostgreSQL: Check container logs and ensure schema is initialized

## Architecture

### Development Mode
```
┌─────────────┐
│   Frontend  │ (Next.js on :3000)
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   Backend   │ (FastAPI on :8000)
└──────┬──────┘
       │
       ├──► SQLite (chatbot.db)
       └──► In-Memory Cache
```

### Docker Mode
```
┌─────────────┐
│   Frontend  │ (Next.js on :3000)
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   Backend   │ (FastAPI on :8000)
└──────┬──────┘
       │
       ├──► PostgreSQL (:5432)
       └──► Redis (:6379)
```

## Makefile Commands

### Development
- `make dev` - Start both backend and frontend (SQLite mode)
- `make dev-backend` - Start only backend
- `make dev-frontend` - Start only frontend

### Docker
- `make docker-up` - Start PostgreSQL + Redis + Backend
- `make docker-stop` - Stop Docker services (keep containers)
- `make docker-down` - Stop and remove Docker services

### Database
- `make db-init` - Initialize database schema
- `make db-migrate` - Run database migrations

### Utilities
- `make stop` - Stop all running services
- `make clean` - Clean build artifacts
- `make help` - Show all available commands

## Next Steps

1. **Get your Anthropic API key:**
   - Sign up at https://console.anthropic.com/
   - Create an API key
   - Add it to `.env` file

2. **Test the application:**
   - Open `http://localhost:3000`
   - Try switching personas: "Act like my mentor", "Be an investor", etc.

3. **Check logs:**
   - Backend logs appear in the terminal
   - Frontend logs appear in browser console

## Support

For issues or questions:
- Check the logs for error messages
- Verify all environment variables are set correctly
- Ensure all dependencies are installed
- Check that ports 3000, 8000, 5432, and 6379 are not in use

