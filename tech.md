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
jeeva_agentic/
│
├── app/                                 # Backend FastAPI application
│   ├── __init__.py
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
├── frontend/                            # Next.js frontend application
│   ├── src/
│   │   ├── app/
│   │   │   ├── chat/
│   │   │   │   └── page.tsx            # Chat interface page
│   │   │   ├── globals.css              # Global styles
│   │   │   ├── layout.tsx               # Root layout
│   │   │   └── page.tsx                 # Home page
│   │   │
│   │   ├── components/
│   │   │   ├── chat/
│   │   │   │   ├── ChatInput.tsx       # Message input component
│   │   │   │   ├── ChatMessage.tsx     # Message display component
│   │   │   │   ├── WelcomeMessage.tsx   # Welcome screen
│   │   │   │   └── index.ts            # Component exports
│   │   │   └── Header.tsx               # Navigation header
│   │   │
│   │   ├── hooks/
│   │   │   └── index.ts                 # React hooks (useChat, useHealth)
│   │   │
│   │   ├── lib/
│   │   │   ├── api.ts                   # API client for backend
│   │   │   └── utils.ts                # Utility functions
│   │   │
│   │   └── types/
│   │       └── index.ts                 # TypeScript type definitions
│   │
│   ├── next.config.js                  # Next.js configuration
│   ├── next-env.d.ts                    # Next.js TypeScript definitions
│   ├── package.json                    # Node.js dependencies
│   ├── postcss.config.js               # PostCSS configuration
│   ├── tailwind.config.ts              # Tailwind CSS configuration
│   └── tsconfig.json                    # TypeScript configuration
│
├── tests/                               # Backend tests
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
│   └── run_migrations.py              # Run SQL migrations
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
├── Makefile                            # Build and run commands
├── requirements.txt                    # Python dependencies
├── pyproject.toml                      # Python project configuration
├── README.md                           # Project documentation
└── tech.md                             # Technical documentation (this file)
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

### **Frontend Application**

#### **`frontend/src/app/chat/page.tsx`**
```typescript
"""Main chat interface page"""
# - Chat message display
# - Persona badge visualization
# - Thread management
# - Integration with useChat hook
```

#### **`frontend/src/lib/api.ts`**
```typescript
"""API client for backend communication"""
# - sendQuery(): POST /chat
# - getChatHistory(): GET /chat_history
# - checkHealth(): GET /health
# - API_BASE_URL configuration
```

#### **`frontend/src/hooks/index.ts`**
```typescript
"""React hooks for chat functionality"""
# - useChat(): Manages chat state, messages, and API calls
# - useHealth(): Monitors backend API health
# - Handles thread_id and persona state
```

#### **`frontend/src/components/chat/ChatMessage.tsx`**
```typescript
"""Message display component"""
# - Shows user and AI messages
# - Displays persona badge with color coding (mentor, investor, technical_advisor, business_expert)
# - Handles message formatting and styling
# - Shows loading and error states
```

#### **`frontend/src/components/chat/ChatInput.tsx`**
```typescript
"""Message input component"""
# - Text input for user messages
# - Submit handler for sending messages
# - Loading state management during API calls
# - Placeholder text for user guidance
```

#### **`frontend/src/components/chat/WelcomeMessage.tsx`**
```typescript
"""Welcome screen component"""
# - Initial welcome message when chat is empty
# - Quick action suggestions for users
# - Onboarding guidance
```

#### **`frontend/package.json`**
```json
"""Node.js dependencies"""
# - Next.js 16
# - React 18
# - TypeScript
# - Tailwind CSS
# - Radix UI components
# - TanStack Query
```

### **Build & Development Tools**

#### **`Makefile`**
```makefile
"""Build automation and development commands"""
# - make install: Install all dependencies (backend + frontend)
# - make dev: Start both backend and frontend in development mode
# - make dev-backend: Start only backend API server
# - make dev-frontend: Start only frontend development server
# - make build: Build both services for production
# - make start: Start both services in production mode
# - make stop: Stop all running services
# - make clean: Clean build artifacts and cache
# - make docker-up: Start services with Docker Compose
# - make docker-down: Stop Docker services
# - make db-init: Initialize database schema
# - make db-migrate: Run database migrations
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

### **Using Makefile (Recommended)**

```bash
# 1. Clone and setup
git clone <repo>
cd jeeva_agentic

# 2. Create .env file
cp .env.example .env
# Add your ANTHROPIC_API_KEY

# 3. Install all dependencies (backend + frontend)
make install

# 4. Start development servers (backend + frontend)
make dev
# Backend: http://localhost:8000
# Frontend: http://localhost:3000

# 5. Or start services separately
make dev-backend    # Start only backend
make dev-frontend   # Start only frontend

# 6. Stop all services
make stop

# 7. Clean build artifacts
make clean
```

### **Using Docker**

```bash
# 1. Clone and setup
git clone <repo>
cd jeeva_agentic

# 2. Create .env file
cp .env.example .env
# Add your ANTHROPIC_API_KEY

# 3. Start with Docker Compose
make docker-up
# Or: docker-compose up --build

# 4. Test API
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "Act like my mentor and help me with product strategy"}'

# 5. Get chat history
curl http://localhost:8000/chat_history?user_id=user123

# 6. Stop Docker services
make docker-down
# Or: docker-compose down
```

### **Manual Setup**

```bash
# Backend Setup
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend Setup
cd frontend
npm install

# Start Backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Start Frontend (in another terminal)
cd frontend
npm run dev
```

---

## **Test Scenarios**

The following test scenarios validate the core persona switching and thread management functionality. These scenarios ensure that:

1. **Persona Persistence**: The agent stays in character until explicitly asked to switch
2. **Thread Isolation**: Each persona maintains its own separate conversation thread
3. **Context Switching**: Switching back to a previous persona recalls the full conversation history
4. **No Accidental Switches**: Only explicit persona switch requests trigger thread changes

### **Test Scenario Workflow**

| Step | User Query | Expected Behavior | Implementation Details |
| :--- | :--- | :--- | :--- |
| **1** | "Act like my mentor" | Create "Mentor" thread | - `detect_persona_switch()` returns `"mentor"`<br>- System creates new thread with `persona="mentor"`<br>- Returns `thread_id` for Mentor thread |
| **2** | "How can I scale?" | Respond as Mentor | - `detect_persona_switch()` returns `None` (no switch detected)<br>- System continues in existing Mentor thread<br>- Bot responds in mentor persona style |
| **3** | "Act like an investor" | **New** Investor thread | - `detect_persona_switch()` returns `"investor"`<br>- System checks for existing Investor thread<br>- If not found, creates new thread with `persona="investor"`<br>- Returns new `thread_id` for Investor thread |
| **4** | "My product is X..." | Respond as Investor | - `detect_persona_switch()` returns `None`<br>- System continues in Investor thread<br>- Bot responds in investor persona style<br>- Context is isolated from Mentor thread |
| **5** | "Back to mentor thread" | Switch to **old** thread | - `detect_persona_switch()` returns `"mentor"`<br>- System finds existing Mentor thread<br>- Switches to that thread's `thread_id`<br>- Full conversation history from Step 1-2 is recalled |

### **Key Behaviors Validated**

#### **1. Persona Persistence (Step 2)**
- **Requirement**: Agent must adopt a persona and *stay* in character until asked to switch
- **Test**: After "Act like my mentor", subsequent messages without explicit switch requests should continue as mentor
- **Implementation**: `detect_persona_switch()` returns `None` when no explicit switch is detected, allowing the system to continue in the current thread

#### **2. Thread Isolation (Step 3-4)**
- **Requirement**: Each persona should have a dedicated, separate conversational thread
- **Test**: Creating an Investor thread should not affect the Mentor thread's context
- **Implementation**: System creates new threads for each persona, maintaining separate `thread_id` values

#### **3. Context Switching (Step 5)**
- **Requirement**: Switching back to a previous persona should recall the full context of that conversation
- **Test**: "Back to mentor thread" should restore the Mentor conversation from Steps 1-2
- **Implementation**: System searches for existing threads by persona and switches to the found thread, preserving all previous messages

#### **4. No Accidental Switches**
- **Requirement**: Only explicit persona switch requests should trigger thread changes
- **Test**: General questions (e.g., "How can I scale?") should not trigger persona switches
- **Implementation**: `detect_persona_switch()` only returns a persona for explicit patterns like "act like", "be my", "switch to", etc.

### **Persona Detection Patterns**

The `detect_persona_switch()` function recognizes the following explicit switch patterns:

1. **Explicit Switch Phrases** (Highest Priority):
   - "act like a mentor" / "act as mentor"
   - "be my mentor" / "be an investor"
   - "switch to mentor" / "switch to investor"
   - "mentor mode" / "investor mode"

2. **Contextual Keywords** (Lower Priority):
   - Only triggers if combined with switch phrases like "as a", "like a", "be my", "be a"
   - Example: "as a mentor" → triggers, but "mentor advice" → does not trigger

3. **Switch Back Patterns**:
   - "back to mentor thread" / "back to mentor mode"
   - "back to investor" / "back to technical"

### **Thread Management Logic**

The chat endpoint implements the following thread switching logic:

```python
if detected_persona_switch:
    # Persona switch requested
    if current_thread.persona == target_persona:
        # Already in correct thread, continue
        use_current_thread()
    else:
        # Need to switch
        existing_thread = find_thread_by_persona(target_persona)
        if existing_thread:
            # Switch to existing thread (recall context)
            switch_to_thread(existing_thread.thread_id)
        else:
            # Create new thread for this persona
            create_new_thread(target_persona)
else:
    # No switch requested
    if current_thread:
        # Continue in existing thread
        continue_in_thread(current_thread.thread_id)
    else:
        # First-time user, create default thread
        create_default_thread()
```

### **Testing the Scenarios**

You can test these scenarios using the API:

```bash
# Step 1: Act like my mentor
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "message": "Act like my mentor"}'
# Save the returned thread_id (e.g., "thread_mentor_123")

# Step 2: Continue as mentor
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "message": "How can I scale?", "thread_id": "thread_mentor_123"}'

# Step 3: Switch to investor
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "message": "Act like an investor"}'
# Save the returned thread_id (e.g., "thread_investor_456")

# Step 4: Continue as investor
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "message": "My product is X...", "thread_id": "thread_investor_456"}'

# Step 5: Switch back to mentor
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "message": "Back to mentor thread"}'
# Should return thread_id: "thread_mentor_123" with full history
```

### **Expected Failures (Before Fix)**

The original implementation had the following issues that these scenarios expose:

1. **Default Persona Bug**: Step 2 would fail because the detector would default to "business_expert" when no keywords were found, causing the thread to switch personas immediately after the first message.

2. **Thread Mutation**: Step 3 would fail because the system would update the existing thread's persona instead of creating a new thread, mixing contexts.

3. **No Context Recall**: Step 5 would fail because the system couldn't switch back to a previous thread - it would just change the current thread's persona again.

These issues have been resolved in the current implementation.

---
