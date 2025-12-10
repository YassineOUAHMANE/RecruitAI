#!/bin/bash

# Script d'arrêt pour l'application docker-compose

cd "$(dirname "$0")" || exit 1

echo "Stopping Docker Compose services..."
echo ""

docker compose down

echo ""
echo "All services stopped successfully!"
echo ""
