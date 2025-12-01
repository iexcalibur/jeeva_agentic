.PHONY: help install install-backend install-frontend dev dev-backend dev-frontend build build-backend build-frontend start start-backend start-frontend stop clean db-init db-migrate test test-backend test-frontend docker-up docker-stop docker-down check-docker check-postgres

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Helper function to check and start Docker
check-docker:
	@if ! docker info > /dev/null 2>&1; then \
		echo "$(YELLOW)Docker is not running. Starting Docker Desktop...$(NC)"; \
		open -a Docker 2>/dev/null || (echo "$(RED)Error: Docker Desktop not found. Please install Docker Desktop from https://www.docker.com/products/docker-desktop$(NC)" && exit 1); \
		echo "$(YELLOW)Waiting for Docker to start...$(NC)"; \
		for i in 1 2 3 4 5 6 7 8 9 10; do \
			if docker info > /dev/null 2>&1; then \
				echo "$(GREEN)✓ Docker is running$(NC)"; \
				break; \
			fi; \
			sleep 2; \
		done; \
		if ! docker info > /dev/null 2>&1; then \
			echo "$(RED)Error: Docker failed to start. Please start Docker Desktop manually.$(NC)"; \
			exit 1; \
		fi; \
	else \
		echo "$(GREEN)✓ Docker is running$(NC)"; \
	fi

# Helper function to check and start PostgreSQL
check-postgres: check-docker
	@POSTGRES_CONTAINER=$$(docker ps -a --format '{{.Names}}' | grep -E '(postgres|jeeva_agentic.*postgres)' | head -1); \
	if [ -z "$$POSTGRES_CONTAINER" ]; then \
		echo "$(YELLOW)PostgreSQL container not found. Starting PostgreSQL...$(NC)"; \
		docker-compose up postgres -d || (echo "$(RED)Error: Failed to start PostgreSQL container$(NC)" && exit 1); \
		echo "$(YELLOW)Waiting for PostgreSQL to be healthy...$(NC)"; \
		for i in 1 2 3 4 5 6 7 8 9 10; do \
			if docker ps --format '{{.Names}} {{.Status}}' | grep -E '(postgres|jeeva_agentic.*postgres)' | grep -q 'healthy'; then \
				echo "$(GREEN)✓ PostgreSQL is running and healthy$(NC)"; \
				break; \
			fi; \
			[ $$i -eq 10 ] && echo "$(YELLOW)PostgreSQL is still starting...$(NC)"; \
			sleep 2; \
		done; \
	elif ! docker ps --format '{{.Names}} {{.Status}}' | grep -E '(postgres|jeeva_agentic.*postgres)' | grep -q 'healthy'; then \
		if docker ps -a --format '{{.Names}} {{.Status}}' | grep -E '(postgres|jeeva_agentic.*postgres)' | grep -q 'Exited'; then \
			echo "$(YELLOW)PostgreSQL container is stopped. Starting...$(NC)"; \
			docker-compose up postgres -d || docker start $$POSTGRES_CONTAINER; \
			sleep 5; \
		else \
			echo "$(YELLOW)PostgreSQL container exists but not healthy. Waiting...$(NC)"; \
			for i in 1 2 3 4 5; do \
				if docker ps --format '{{.Names}} {{.Status}}' | grep -E '(postgres|jeeva_agentic.*postgres)' | grep -q 'healthy'; then \
					echo "$(GREEN)✓ PostgreSQL is running and healthy$(NC)"; \
					break; \
				fi; \
				sleep 2; \
			done; \
		fi; \
	else \
		echo "$(GREEN)✓ PostgreSQL is running and healthy$(NC)"; \
	fi

help: ## Show this help message
	@echo "$(BLUE)Jeeva Agentic - Makefile Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Installation:$(NC)"
	@echo "  make install              - Install all dependencies (backend + frontend)"
	@echo "  make install-backend      - Install backend Python dependencies"
	@echo "  make install-frontend     - Install frontend Node.js dependencies"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make dev                  - Start both backend and frontend (SQLite + in-memory cache)"
	@echo "  make dev-backend          - Start only backend API server (SQLite + in-memory cache)"
	@echo "  make dev-frontend         - Start only frontend development server"
	@echo ""
	@echo "$(GREEN)Production:$(NC)"
	@echo "  make build                - Build both backend and frontend"
	@echo "  make build-backend        - Build backend only"
	@echo "  make build-frontend       - Build frontend only"
	@echo "  make start                - Start both services in production mode"
	@echo ""
	@echo "$(GREEN)Database:$(NC)"
	@echo "  make db-init              - Initialize database schema"
	@echo "  make db-migrate           - Run database migrations"
	@echo ""
	@echo "$(GREEN)Docker:$(NC)"
	@echo "  make docker-up             - Start services with Docker Compose (PostgreSQL + Redis)"
	@echo "  make docker-stop           - Stop Docker services (keeps containers)"
	@echo "  make docker-down           - Stop and remove Docker services"
	@echo ""
	@echo "$(GREEN)Testing:$(NC)"
	@echo "  make test                 - Run all tests"
	@echo "  make test-backend         - Run backend tests"
	@echo ""
	@echo "$(GREEN)Utilities:$(NC)"
	@echo "  make clean                - Clean build artifacts and cache"
	@echo "  make stop                 - Stop all running services"

# Installation
install: install-backend install-frontend ## Install all dependencies

install-backend: ## Install backend Python dependencies
	@echo "$(BLUE)Installing backend dependencies...$(NC)"
	@if [ ! -d "venv" ]; then \
		echo "$(YELLOW)Creating virtual environment...$(NC)"; \
		python3.12 -m venv venv || python3.11 -m venv venv || python3 -m venv venv; \
	fi
	@echo "$(YELLOW)Activating virtual environment and installing packages...$(NC)"
	@. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "$(GREEN)✓ Backend dependencies installed$(NC)"

install-frontend: ## Install frontend Node.js dependencies
	@echo "$(BLUE)Installing frontend dependencies...$(NC)"
	@cd frontend && npm install
	@echo "$(GREEN)✓ Frontend dependencies installed$(NC)"

# Development
dev: ## Start both backend and frontend in development mode (SQLite + in-memory cache)
	@echo "$(BLUE)Starting development servers...$(NC)"
	@echo "$(YELLOW)Mode: SQLite + In-Memory Cache$(NC)"
	@echo "$(YELLOW)Backend: http://localhost:8000$(NC)"
	@echo "$(YELLOW)Frontend: http://localhost:3000$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to stop all services$(NC)"
	@cleanup() { \
		echo ""; \
		echo "$(YELLOW)Stopping all services...$(NC)"; \
		pkill -f "uvicorn app.main:app" 2>/dev/null || true; \
		pkill -f "next dev" 2>/dev/null || true; \
		echo "$(GREEN)✓ All services stopped$(NC)"; \
		exit 0; \
	}; \
	trap cleanup INT TERM EXIT; \
	make dev-backend & \
	BACKEND_PID=$$!; \
	make dev-frontend & \
	FRONTEND_PID=$$!; \
	wait $$BACKEND_PID $$FRONTEND_PID || true; \
	trap - INT TERM EXIT

dev-backend: ## Start backend API server (SQLite + in-memory cache)
	@echo "$(BLUE)Starting backend server (SQLite mode)...$(NC)"
	@if [ ! -d "venv" ]; then \
		echo "$(YELLOW)Virtual environment not found. Run 'make install-backend' first$(NC)"; \
		exit 1; \
	fi
	@. venv/bin/activate && \
	if [ ! -f ".env" ]; then \
		echo "$(YELLOW)Creating .env file for SQLite mode...$(NC)"; \
		cat > .env << 'EOF' \
DATABASE_TYPE=sqlite \
CACHE_TYPE=memory \
SQLITE_DB_PATH=chatbot.db \
ANTHROPIC_API_KEY=your_anthropic_api_key_here \
LOG_LEVEL=INFO \
DEBUG=false \
EOF \
		echo "$(YELLOW)⚠️  Please update ANTHROPIC_API_KEY in .env file$(NC)"; \
	fi; \
	echo "$(YELLOW)Initializing SQLite database schema...$(NC)"; \
	PYTHONPATH=$$(pwd) python scripts/init_db.py 2>/dev/null || echo "$(YELLOW)Database may already be initialized$(NC)"; \
	echo "$(GREEN)Starting FastAPI server...$(NC)"; \
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Start frontend development server
	@echo "$(BLUE)Starting frontend server...$(NC)"
	@cd frontend && npm run dev

# Production Build
build: build-backend build-frontend ## Build both backend and frontend

build-backend: ## Build backend (no build step needed for Python)
	@echo "$(GREEN)✓ Backend is ready (Python doesn't require compilation)$(NC)"

build-frontend: ## Build frontend for production
	@echo "$(BLUE)Building frontend...$(NC)"
	@cd frontend && npm run build
	@echo "$(GREEN)✓ Frontend built successfully$(NC)"

# Production Start
start: ## Start both services in production mode
	@echo "$(BLUE)Starting production servers...$(NC)"
	@trap 'kill 0' EXIT; \
	make start-backend & \
	make start-frontend & \
	wait

start-backend: ## Start backend in production mode
	@echo "$(BLUE)Starting backend in production mode...$(NC)"
	@. venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000

start-frontend: ## Start frontend in production mode
	@echo "$(BLUE)Starting frontend in production mode...$(NC)"
	@cd frontend && npm run start

# Database
db-init: ## Initialize database schema (SQLite for dev, PostgreSQL for docker)
	@echo "$(BLUE)Initializing database...$(NC)"
	@. venv/bin/activate && PYTHONPATH=$$(pwd) python scripts/init_db.py

db-migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(NC)"
	@. venv/bin/activate && python scripts/run_migrations.py

# Docker
docker-up: check-docker ## Start services with Docker Compose (PostgreSQL + Redis)
	@echo "$(BLUE)Starting Docker services (PostgreSQL + Redis)...$(NC)"
	@docker-compose up --build -d
	@echo "$(GREEN)✓ Docker services started$(NC)"
	@echo "$(YELLOW)PostgreSQL: localhost:5432$(NC)"
	@echo "$(YELLOW)Redis: localhost:6379$(NC)"
	@echo "$(YELLOW)Backend API: http://localhost:8000$(NC)"

docker-down: ## Stop and remove Docker services (removes containers and volumes)
	@echo "$(BLUE)Stopping and removing Docker services...$(NC)"
	@docker-compose down
	@echo "$(GREEN)✓ Docker services stopped and removed$(NC)"

docker-stop: ## Stop Docker services but keep containers (data preserved)
	@echo "$(BLUE)Stopping Docker services...$(NC)"
	@docker-compose stop
	@echo "$(GREEN)✓ Docker services stopped (containers preserved)$(NC)"

# Testing
test: test-backend ## Run all tests

test-backend: ## Run backend tests
	@echo "$(BLUE)Running backend tests...$(NC)"
	@. venv/bin/activate && pytest

# Utilities
clean: ## Clean build artifacts and cache
	@echo "$(BLUE)Cleaning...$(NC)"
	@rm -rf __pycache__ app/__pycache__ app/**/__pycache__
	@rm -rf .pytest_cache .coverage htmlcov
	@rm -rf frontend/.next frontend/node_modules/.cache
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Cleaned$(NC)"

stop: ## Stop all running services
	@echo "$(BLUE)Stopping services...$(NC)"
	@pkill -f "uvicorn app.main:app" 2>/dev/null || true
	@pkill -f "next dev" 2>/dev/null || true
	@docker-compose stop postgres redis 2>/dev/null || true
	@echo "$(GREEN)✓ All services stopped$(NC)"
	@echo "$(YELLOW)Note: Docker containers are stopped but not removed. Run 'make docker-down' to remove them.$(NC)"

