# Jeeva Agentic

A sophisticated chatbot application that can switch between different personas (mentor, investor, technical advisor, business expert) using LangGraph for agentic state management.

## Features

- **Persona Switching**: Automatically detects and switches between different personas based on user intent
- **Persistent Memory**: PostgreSQL-backed conversation history and state management
- **LangGraph Integration**: Stateful agent orchestration with checkpointing
- **FastAPI Backend**: Async REST API for chat interactions
- **Next.js Frontend**: Modern React-based frontend interface with persona visualization
- **Docker Support**: Easy deployment with Docker Compose

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Next.js 16, React, TypeScript, Tailwind CSS
- **Orchestration**: LangGraph
- **Database**: PostgreSQL with Asyncpg
- **LLM**: Claude 3.5 Sonnet (Anthropic API)

## Quick Start

### Prerequisites

- **Python 3.11 or 3.12** (required for backend)
- **Node.js 20+** and **npm 10+** (required for frontend)
- Docker and Docker Compose (optional, for containerized setup)
- Anthropic API Key

### Installation

```bash
# Clone the repository
git clone <repo>
cd jeeva_agentic

# Install all dependencies (backend + frontend)
make install
```

### Development

```bash
# Start both backend and frontend in development mode
make dev
```

This will start:
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

### Available Make Commands

```bash
make help              # Show all available commands
make install           # Install all dependencies
make dev               # Start both backend and frontend
make dev-backend       # Start only backend
make dev-frontend      # Start only frontend
make build             # Build for production
make test              # Run tests
make docker-up         # Start with Docker Compose
make clean             # Clean build artifacts
```

### Environment Setup

Create a `.env` file in the root directory:

```bash
DATABASE_URL=postgresql://chatbot_user:chatbot_pass@localhost:5432/chatbot_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=chatbot_user
POSTGRES_PASSWORD=chatbot_pass
POSTGRES_DB=chatbot_db
ANTHROPIC_API_KEY=your_anthropic_api_key_here
LOG_LEVEL=INFO
DEBUG=false
```

**Important:** Replace `your_anthropic_api_key_here` with your actual Anthropic API key.

## Project Structure

```
jeeva_agentic/
├── app/                    # Backend FastAPI application
│   ├── main.py            # FastAPI entry point
│   ├── api/               # API routes
│   ├── services/          # Business logic (agent, LLM, memory)
│   ├── database/          # Database connection and migrations
│   └── core/              # Configuration and utilities
├── frontend/              # Next.js frontend application
│   ├── src/
│   │   ├── app/           # Next.js app router pages
│   │   ├── components/    # React components
│   │   └── lib/           # Utilities and API client
│   └── package.json       # Frontend dependencies
├── scripts/               # Utility scripts
├── tests/                 # Test files
├── docker/                # Docker configuration
├── Makefile               # Build and run commands
├── requirements.txt       # Python dependencies
└── docker-compose.yml     # Docker Compose configuration
```

## Development Workflow

### Backend Development

```bash
# Start backend only
make dev-backend

# Run database migrations
make db-init

# Run tests
make test-backend
```

### Frontend Development

```bash
# Start frontend only
make dev-frontend

# Build for production
make build-frontend
```

### Full Stack Development

```bash
# Start both services
make dev

# Stop all services
make stop
```

## API Integration

The frontend is configured to connect to the backend API at `http://localhost:8000/api`. 

**Note:** The frontend currently uses placeholder API endpoints. Update `frontend/src/lib/api.ts` to integrate with the backend chat endpoints:
- `/api/chat` - Send chat messages
- `/api/chat_history` - Get conversation history

See `app/api/routes/` for available backend endpoints.

## Testing

```bash
# Run all tests
make test

# Run backend tests only
make test-backend
```

## Docker Deployment

```bash
# Start all services with Docker
make docker-up

# Stop Docker services
make docker-down
```

## License

MIT License
