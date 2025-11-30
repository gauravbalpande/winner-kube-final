.PHONY: help install dev build test clean docker-up docker-down migrate

help:
	@echo "BetMasterX - Available Commands:"
	@echo "  make install      - Install all dependencies"
	@echo "  make dev          - Run development servers"
	@echo "  make build        - Build production artifacts"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make migrate      - Run database migrations"

install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

dev:
	@echo "Starting development servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	make -j 2 dev-backend dev-frontend

dev-backend:
	cd backend && uvicorn main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

build:
	@echo "Building production artifacts..."
	cd frontend && npm run build
	@echo "Build complete!"

docker-up:
	@echo "Starting Docker containers..."
	docker-compose up -d
	@echo "Services started!"
	@echo "Frontend: http://localhost:5173"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

docker-logs:
	docker-compose logs -f

migrate:
	@echo "Running database migrations..."
	@echo "Please run migrations through Supabase Dashboard or psql"

clean:
	@echo "Cleaning build artifacts..."
	rm -rf backend/__pycache__
	rm -rf backend/**/__pycache__
	rm -rf frontend/dist
	rm -rf frontend/node_modules
	@echo "Clean complete!"

test:
	@echo "Running tests..."
	cd backend && pytest
	@echo "Tests complete!"