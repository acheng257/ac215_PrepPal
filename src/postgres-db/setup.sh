#!/bin/bash

# Stop and remove existing container
docker stop postgresdb_preppal 2>/dev/null || true
docker rm postgresdb_preppal 2>/dev/null || true

# Check if an image with the name exists, and remove it if it does
IMAGE_ID=$(docker images -q postgresdb_preppal)
if [ -n "$IMAGE_ID" ]; then
  docker rmi "$IMAGE_ID"
else
  echo "No existing image with the name 'postgresdb_preppal' found."
fi

# Remove the volume to ensure a clean setup
# docker volume rm postgres-db_db_data || true

# Build and run the container
docker compose up --build -d
