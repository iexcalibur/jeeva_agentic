# Persona Switching Chatbot

A sophisticated chatbot application that can switch between different personas (mentor, investor, technical advisor, business expert) using LangGraph for agentic state management.

## Features

- **Persona Switching**: Automatically detects and switches between different personas based on user intent
- **Persistent Memory**: PostgreSQL-backed conversation history and state management
- **LangGraph Integration**: Stateful agent orchestration with checkpointing
- **FastAPI Backend**: Async REST API for chat interactions
- **Docker Support**: Easy deployment with Docker Compose

## Tech Stack

- **Orchestration**: LangGraph
- **Backend**: FastAPI
- **Database**: PostgreSQL with Asyncpg
- **LLM**: Claude 3.5 Sonnet (Anthropic API)
- **Language**: Python 3.10+

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Anthropic API Key

### Setup

1. Clone the repository:
```bash
git clone <repo>
cd persona-switching-chatbot
```

2. Create `.env` file:
```bash
# Create .env file with the following content:
cat > .env << EOF
DATABASE_URL=postgresql://chatbot_user:chatbot_pass@localhost:5432/chatbot_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=chatbot_user
POSTGRES_PASSWORD=chatbot_pass
POSTGRES_DB=chatbot_db
ANTHROPIC_API_KEY=your_anthropic_api_key_here
LOG_LEVEL=INFO
DEBUG=false
EOF
```

3. Start with Docker:
```bash
docker-compose up --build
```

4. Test the API:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "Act like my mentor and help me with product strategy"}'
```

5. Get chat history:
```bash
curl http://localhost:8000/chat_history?user_id=user123
```

## Development

### Local Development (without Docker)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start PostgreSQL (or use Docker):
```bash
docker-compose up postgres -d
```

3. Run migrations:
```bash
python scripts/init_db.py
```

4. Start the application:
```bash
uvicorn app.main:app --reload
```

## Project Structure

See `tech.md` for complete folder structure and file descriptions.

# jeeva_agentic
