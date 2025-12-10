#!/bin/bash

# Script de démarrage pour l'application docker-compose

set -e

cd "$(dirname "$0")" || exit 1

echo "=========================================="
echo "HR ASSISTANT - DOCKER COMPOSE STARTUP"
echo "=========================================="
echo ""

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed"
    exit 1
fi

echo "Docker version: $(docker --version)"
echo ""

# Vérifier que le fichier .env existe
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found in src directory"
    echo "Please create src/.env with required environment variables"
    exit 1
fi

echo "Starting Docker Compose services..."
echo ""

# Démarrer les services
docker compose up -d

echo ""
echo "=========================================="
echo "Services starting up..."
echo "=========================================="
echo ""
echo "Waiting for services to be ready..."
sleep 10

echo ""
echo "Service Status:"
docker compose ps

echo ""
echo "=========================================="
echo "Application is starting!"
echo "=========================================="
echo ""
echo "Access points:"
echo "  - API (FastAPI):      http://localhost:8000"
echo "  - API Docs (Swagger): http://localhost:8000/docs"
echo "  - Frontend (React):   http://localhost:8001"
echo "  - Database (MySQL):   localhost:3306"
echo "  - Vector DB (Qdrant): localhost:6333"
echo ""
echo "View logs:"
echo "  docker compose logs -f"
echo ""
echo "Stop services:"
echo "  docker compose down"
echo ""
echo "=========================================="
