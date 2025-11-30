.PHONY: help install install-backend install-frontend dev dev-backend dev-frontend build build-backend build-frontend start start-backend start-frontend stop clean db-init db-migrate test test-backend test-frontend docker-up docker-down

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Jeeva Agentic - Makefile Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Installation:$(NC)"
	@echo "  make install              - Install all dependencies (backend + frontend)"
	@echo "  make install-backend      - Install backend Python dependencies"
	@echo "  make install-frontend     - Install frontend Node.js dependencies"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make dev                  - Start both backend and frontend in development mode"
	@echo "  make dev-backend          - Start only backend API server"
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
	@echo "  make docker-up             - Start services with Docker Compose"
	@echo "  make docker-down           - Stop Docker services"
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
dev: ## Start both backend and frontend in development mode
	@echo "$(BLUE)Starting development servers...$(NC)"
	@echo "$(YELLOW)Backend: http://localhost:8000$(NC)"
	@echo "$(YELLOW)Frontend: http://localhost:3000$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to stop all services$(NC)"
	@trap 'kill 0' EXIT; \
	make dev-backend & \
	make dev-frontend & \
	wait

dev-backend: ## Start backend API server
	@echo "$(BLUE)Starting backend server...$(NC)"
	@if [ ! -d "venv" ]; then \
		echo "$(YELLOW)Virtual environment not found. Run 'make install-backend' first$(NC)"; \
		exit 1; \
	fi
	@. venv/bin/activate && \
	if [ ! -f ".env" ]; then \
		echo "$(YELLOW)Creating .env file...$(NC)"; \
		cat > .env << 'EOF' \
DATABASE_URL=postgresql://chatbot_user:chatbot_pass@localhost:5432/chatbot_db \
POSTGRES_HOST=localhost \
POSTGRES_PORT=5432 \
POSTGRES_USER=chatbot_user \
POSTGRES_PASSWORD=chatbot_pass \
POSTGRES_DB=chatbot_db \
ANTHROPIC_API_KEY=your_anthropic_api_key_here \
LOG_LEVEL=INFO \
DEBUG=false \
EOF \
		echo "$(YELLOW)⚠️  Please update ANTHROPIC_API_KEY in .env file$(NC)"; \
	fi; \
	docker-compose up postgres -d 2>/dev/null || true; \
	sleep 2; \
	python scripts/init_db.py 2>/dev/null || true; \
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
db-init: ## Initialize database schema
	@echo "$(BLUE)Initializing database...$(NC)"
	@. venv/bin/activate && python scripts/init_db.py

db-migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(NC)"
	@. venv/bin/activate && python scripts/run_migrations.py

# Docker
docker-up: ## Start services with Docker Compose
	@echo "$(BLUE)Starting Docker services...$(NC)"
	@docker-compose up --build -d
	@echo "$(GREEN)✓ Docker services started$(NC)"

docker-down: ## Stop Docker services
	@echo "$(BLUE)Stopping Docker services...$(NC)"
	@docker-compose down
	@echo "$(GREEN)✓ Docker services stopped$(NC)"

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
	@docker-compose down 2>/dev/null || true
	@echo "$(GREEN)✓ All services stopped$(NC)"

