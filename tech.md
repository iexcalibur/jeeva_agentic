# Tech Stack & Complete Folder Structure

## **Tech Stack**

### **Core Technologies**
- **Orchestration:** LangGraph (for agentic state management)
- **Backend:** FastAPI (async web framework)
- **Database:** PostgreSQL with Asyncpg driver
- **LLM:** Claude 3.5 Sonnet (Anthropic API)
- **Language:** Python 3.10+
- **Validation:** Pydantic v2
- **Deployment:** Docker & Docker Compose

### **Supporting Libraries**
- **langchain-anthropic:** Claude integration
- **langgraph:** State graph management
- **asyncpg:** Async PostgreSQL driver
- **uvicorn:** ASGI server
- **python-dotenv:** Environment management
- **pytest + pytest-asyncio:** Testing

---

## **Complete Folder Structure**

```
persona-switching-chatbot/
│
├── app/
│   ├── __init__.py
│   │
│   ├── main.py                         # FastAPI application entry point
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py                 # /chat endpoint
│   │   │   └── history.py              # /chat_history endpoint
│   │   └── dependencies.py             # Dependency injection (DB, agent)
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                   # Settings & environment variables
│   │   ├── logging.py                  # Logging configuration
│   │   └── exceptions.py               # Custom exception handlers
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py                  # Pydantic models (request/response)
│   │   └── database.py                 # Database table definitions
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent/
│   │   │   ├── __init__.py
│   │   │   ├── graph.py                # LangGraph state graph definition
│   │   │   ├── nodes.py                # Agent nodes (persona logic)
│   │   │   ├── state.py                # State schema definition
│   │   │   └── prompts.py              # System prompts for personas
│   │   │
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   └── claude.py               # Claude API wrapper
│   │   │
│   │   └── memory/
│   │       ├── __init__.py
│   │       ├── checkpointer.py         # Custom PostgreSQL checkpointer
│   │       └── thread_manager.py       # Thread CRUD operations
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py               # Database connection pool
│   │   ├── migrations/
│   │   │   ├── 001_initial_schema.sql  # Initial DB schema
│   │   │   └── 002_add_indexes.sql     # Performance indexes
│   │   └── queries.py                  # Raw SQL queries
│   │
│   └── utils/
│       ├── __init__.py
│       ├── persona_detector.py         # Detect persona switch intent
│       └── validators.py               # Custom validation logic
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                     # Pytest fixtures
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_chat.py
│   │   └── test_history.py
│   ├── test_services/
│   │   ├── __init__.py
│   │   ├── test_agent.py
│   │   └── test_thread_manager.py
│   └── test_integration/
│       ├── __init__.py
│       └── test_persona_switching.py
│
├── scripts/
│   ├── init_db.py                      # Initialize database schema
│   ├── seed_data.py                    # Seed test data (optional)
│   └── run_migrations.py               # Run SQL migrations
│
├── docker/
│   ├── Dockerfile                      # Application container
│   └── postgres/
│       └── init.sql                    # PostgreSQL initialization
│
├── .env.example                        # Example environment variables
├── .env                                # Actual environment variables (gitignored)
├── .gitignore
├── docker-compose.yml                  # Multi-container orchestration
├── requirements.txt                    # Python dependencies
├── pyproject.toml                      # Python project configuration
└── README.md                           # Project documentation
```

---

## **Key File Descriptions**

### **Core Application Files**

#### **`app/main.py`**
```python
"""FastAPI application entry point"""
# - Initialize FastAPI app
# - Include routers
# - Setup middleware (CORS, logging)
# - Lifespan events (DB connection pool)
```

#### **`app/core/config.py`**
```python
"""Configuration management"""
# - DATABASE_URL
# - ANTHROPIC_API_KEY
# - POSTGRES_HOST, POSTGRES_PORT, etc.
# - LOG_LEVEL
# Uses Pydantic Settings for validation
```

### **Agent Architecture**

#### **`app/services/agent/graph.py`**
```python
"""LangGraph state graph definition"""
# - Define agent nodes (route_persona, execute_persona, save_context)
# - Define edges (conditional routing)
# - Compile graph with PostgreSQL checkpointer
```

#### **`app/services/agent/state.py`**
```python
"""Agent state schema"""
# - messages: List[BaseMessage]
# - current_persona: str
# - thread_id: str
# - user_id: str
# - metadata: dict
```

#### **`app/services/agent/prompts.py`**
```python
"""System prompts for personas"""
PERSONAS = {
    "mentor": "You are a supportive mentor...",
    "investor": "You are a skeptical investor...",
    "technical_advisor": "You are a technical expert...",
    # Base meta-persona
    "business_expert": "You are a Business Domain Expert..."
}
```

### **Database Layer**

#### **`app/database/connection.py`**
```python
"""Asyncpg connection pool management"""
# - create_pool()
# - get_connection()
# - close_pool()
```

#### **`app/services/memory/checkpointer.py`**
```python
"""Custom PostgreSQL checkpointer for LangGraph"""
# - Implements BaseCheckpointSaver
# - save() method writes to PostgreSQL
# - load() method retrieves thread state
```

#### **`app/database/migrations/001_initial_schema.sql`**
```sql
-- Users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Threads table
CREATE TABLE threads (
    thread_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    persona VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Messages table
CREATE TABLE messages (
    message_id UUID PRIMARY KEY,
    thread_id UUID REFERENCES threads(thread_id),
    role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Checkpoints table (for LangGraph state)
CREATE TABLE checkpoints (
    checkpoint_id UUID PRIMARY KEY,
    thread_id UUID REFERENCES threads(thread_id),
    state JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### **API Layer**

#### **`app/api/routes/chat.py`**
```python
"""Chat endpoint"""
@router.post("/chat")
async def chat(request: ChatRequest, agent: Agent = Depends(get_agent)):
    # 1. Detect persona switch intent
    # 2. Route to appropriate thread (new or existing)
    # 3. Invoke LangGraph agent
    # 4. Return response
```

#### **`app/api/routes/history.py`**
```python
"""Chat history endpoint"""
@router.get("/chat_history")
async def get_chat_history(user_id: str, thread_id: Optional[str] = None):
    # 1. Query database for user's threads
    # 2. Return formatted conversation history
```

#### **`app/models/schemas.py`**
```python
"""Pydantic request/response models"""
class ChatRequest(BaseModel):
    user_id: str
    message: str
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    thread_id: str
    persona: str
    response: str
    created_at: datetime
```

---

## **Docker Configuration**

### **`docker-compose.yml`**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: chatbot_user
      POSTGRES_PASSWORD: chatbot_pass
      POSTGRES_DB: chatbot_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U chatbot_user"]
      interval: 5s
      timeout: 5s
      retries: 5

  app:
    build:
      context: .
      dockerfile: docker/Dockerfile
    environment:
      DATABASE_URL: postgresql://chatbot_user:chatbot_pass@postgres:5432/chatbot_db
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres_data:
```

### **`docker/Dockerfile`**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run migrations on startup
CMD ["sh", "-c", "python scripts/init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

---

## **Dependencies (`requirements.txt`)**

```txt
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# LangChain & LangGraph
langchain==0.1.0
langchain-anthropic==0.1.0
langgraph==0.0.20
langchain-core==0.1.0

# Database
asyncpg==0.29.0

# Utilities
python-dotenv==1.0.0
python-multipart==0.0.6

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# Development
black==23.12.0
ruff==0.1.8
```

---

## **Quick Start Commands**

```bash
# 1. Clone and setup
git clone <repo>
cd persona-switching-chatbot

# 2. Create .env file
cp .env.example .env
# Add your ANTHROPIC_API_KEY

# 3. Start with Docker
docker-compose up --build

# 4. Test API
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "Act like my mentor and help me with product strategy"}'

# 5. Get chat history
curl http://localhost:8000/chat_history?user_id=user123
```

---
