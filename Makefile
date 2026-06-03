.PHONY: help install dev run test clean docker-build docker-up docker-down deploy lint format check-redis

help:
	@echo "URL Resolution Engine - Makefile Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install       - Install dependencies"
	@echo "  make dev           - Run development server with auto-reload"
	@echo "  make dev-no-redis  - Run development server WITHOUT Redis (quick testing)"
	@echo "  make run           - Run production server"
	@echo "  make run-no-redis  - Run production server WITHOUT Redis"
	@echo "  make test          - Run API tests"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-up     - Start services with docker-compose"
	@echo "  make docker-down   - Stop services"
	@echo ""
	@echo "Maintenance:"
	@echo "  make lint          - Run code linting"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean temporary files"
	@echo "  make check-redis   - Verify Redis connection"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy        - Deploy to production (requires sudo)"

# Development commands
install:
	pip install -r requirements.txt

dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

dev-no-redis:
	@echo "Starting development server WITHOUT Redis caching..."
	ENABLE_REDIS=false uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

run:
	python main.py

run-no-redis:
	@echo "Starting production server WITHOUT Redis caching..."
	ENABLE_REDIS=false python main.py

test:
	@echo "Starting API test suite..."
	@sleep 2
	python test_api.py

# Docker commands
docker-build:
	docker build -t url-resolver:latest .

docker-up:
	docker-compose up -d
	@echo "Waiting for services to start..."
	@sleep 5
	@docker-compose ps
	@echo ""
	@echo "Services are running. Access API at http://localhost:8000"
	@echo "View logs: docker-compose logs -f"

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Maintenance commands
lint:
	@echo "Running flake8..."
	@pip install flake8 > /dev/null 2>&1
	@flake8 main.py --max-line-length=120 --ignore=E501,W503 || echo "Note: Install flake8 for linting"

format:
	@echo "Formatting code with black..."
	@pip install black > /dev/null 2>&1
	@black main.py test_api.py --line-length=120 || echo "Note: Install black for formatting"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true
	rm -rf .pytest_cache build dist *.egg-info 2>/dev/null || true
	@echo "Cleaned temporary files"

check-redis:
	@echo "Checking Redis connection..."
	@redis-cli ping || echo "Redis is not running. Start with: redis-server"

# Production deployment
deploy:
	@echo "Deploying to production..."
	@bash deploy/scripts/deploy.sh production

# Health check
health:
	@curl -s http://localhost:8000/health | python -m json.tool || echo "Service not running"

# Quick test endpoint
quick-test:
	@echo "Testing health endpoint..."
	@curl -s http://localhost:8000/health
	@echo ""
	@echo ""
	@echo "Testing resolve endpoint (will fail with 403 - expected)..."
	@curl -s -X POST http://localhost:8000/api/v1/resolve \
		-H "Content-Type: application/json" \
		-d '{"url":"https://test.com?surl=test"}'
	@echo ""

# Setup development environment
setup:
	@echo "Setting up development environment..."
	python3 -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"
	@echo "Then run: make install"
