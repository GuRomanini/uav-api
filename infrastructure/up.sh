#!/bin/bash
echo "Stop running services..."
docker-compose -f ./infrastructure/docker-compose.yml stop
echo "Removing existing services..."
docker-compose -f ./infrastructure/docker-compose.yml rm
echo "Building app..."
docker-compose -f ./infrastructure/docker-compose.yml build
echo "Runing app.."
docker-compose -f ./infrastructure/docker-compose.yml up
