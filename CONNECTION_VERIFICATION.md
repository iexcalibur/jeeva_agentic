# Connection Verification Guide

This document verifies that all connections are properly set up between frontend, backend, database, and cache.

## ✅ Connection Status

### Frontend ↔ Backend
- **Status**: ✅ Configured
- **Frontend API URL**: `http://localhost:8000` (default)
- **Backend CORS**: Enabled for all origins in development
- **Endpoints**:
  - `GET /health` - Health check
  - `POST /api/chat` - Send chat message
  - `GET /api/chat_history` - Get chat history

### Backend ↔ Database

#### Development Mode (SQLite)
- **Status**: ✅ Configured
- **Database**: SQLite (`chatbot.db`)
- **Connection**: File-based, no network required
- **Schema**: Auto-initialized on first run

#### Docker Mode (PostgreSQL)
- **Status**: ✅ Configured
- **Database**: PostgreSQL
- **Host**: `localhost:5432` (or `postgres:5432` in Docker network)
- **Connection String**: `postgresql://chatbot_user:chatbot_pass@localhost:5432/chatbot_db`
- **Schema**: Auto-initialized via migrations

### Backend ↔ Cache

#### Development Mode (In-Memory)
- **Status**: ✅ Configured
- **Cache Type**: Python dictionary (in-memory)
- **Persistence**: None (cleared on restart)
- **No external service required**

#### Docker Mode (Redis)
- **Status**: ✅ Configured
- **Cache Type**: Redis
- **Host**: `localhost:6379` (or `redis:6379` in Docker network)
- **Database**: 0 (default)
- **Persistence**: Enabled (AOF)

## Verification Steps

### 1. Verify Backend Health

```bash
# Development mode
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy"}
```

### 2. Verify Database Connection

#### SQLite (Development)
```bash
# Check if database file exists
ls -la chatbot.db

# Should show the database file
```

#### PostgreSQL (Docker)
```bash
# Check PostgreSQL container
docker ps | grep postgres

# Test connection
docker-compose exec postgres psql -U chatbot_user -d chatbot_db -c "SELECT 1;"
```

### 3. Verify Redis Connection (Docker Mode)

```bash
# Check Redis container
docker ps | grep redis

# Test connection
docker-compose exec redis redis-cli ping

# Expected: PONG
```

### 4. Verify Frontend Connection

1. **Start the application:**
   ```bash
   make dev
   ```

2. **Open browser:**
   - Navigate to `http://localhost:3000`
   - Open browser DevTools (F12)
   - Check Console tab for errors
   - Check Network tab for API calls

3. **Test API call:**
   ```bash
   curl http://localhost:8000/api/chat \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"user_id": "test-user-123", "message": "Hello, test message"}'
   ```

### 5. End-to-End Test

1. **Start services:**
   ```bash
   make dev
   ```

2. **Open frontend:**
   - Go to `http://localhost:3000`
   - Send a test message: "Act like my mentor"
   - Verify response appears

3. **Check backend logs:**
   - Should show database connection
   - Should show cache initialization
   - Should show API request processing

## Troubleshooting

### Frontend can't connect to backend

**Symptoms:**
- Frontend shows "API Not Connected"
- Network errors in browser console
- CORS errors

**Solutions:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check backend logs for errors
3. Verify CORS settings in `app/main.py`
4. Check that frontend is using correct API URL

### Database connection errors

**SQLite (Development):**
- Ensure `chatbot.db` file exists
- Run `make db-init` to recreate database
- Check file permissions

**PostgreSQL (Docker):**
- Verify Docker is running: `docker ps`
- Check PostgreSQL container: `docker-compose logs postgres`
- Verify connection string in `.env`
- Test connection: `docker-compose exec postgres psql -U chatbot_user -d chatbot_db`

### Redis connection errors (Docker mode)

**Symptoms:**
- Cache operations fail
- Backend logs show Redis connection errors

**Solutions:**
1. Check Redis container: `docker ps | grep redis`
2. Test Redis: `docker-compose exec redis redis-cli ping`
3. Check Redis logs: `docker-compose logs redis`
4. Verify Redis settings in `.env`

## Configuration Files

### Development Mode (.env)
```env
DATABASE_TYPE=sqlite
CACHE_TYPE=memory
SQLITE_DB_PATH=chatbot.db
ANTHROPIC_API_KEY=your_key_here
```

### Docker Mode (.env)
```env
USE_DOCKER=true
DATABASE_TYPE=postgresql
CACHE_TYPE=redis
DATABASE_URL=postgresql://chatbot_user:chatbot_pass@localhost:5432/chatbot_db
REDIS_HOST=localhost
REDIS_PORT=6379
```

## Summary

✅ **All connections are properly configured:**
- Frontend → Backend: HTTP API calls
- Backend → Database: SQLite (dev) or PostgreSQL (docker)
- Backend → Cache: In-memory (dev) or Redis (docker)

The application automatically detects the mode based on environment variables and configures connections accordingly.

