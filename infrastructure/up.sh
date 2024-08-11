#!/bin/bash
echo "Removing existing services..."
docker-compose rm
echo "Building app..."
docker-compose build
echo "Runing app.."
docker-compose up
