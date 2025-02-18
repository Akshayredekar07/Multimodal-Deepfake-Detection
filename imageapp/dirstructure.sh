#!/bin/bash

# Create the main project directory
mkdir -p fastapi_model_serving

# Navigate into the project directory
cd fastapi_model_serving

# Create directories for the FastAPI app
mkdir -p app
mkdir -p app/models
mkdir -p app/routers
mkdir -p app/utils

# Create directories for configuration and static files
mkdir -p config
mkdir -p static

# Create directories for tests
mkdir -p tests
mkdir -p tests/unit
mkdir -p tests/integration

# Create a directory for Docker and deployment files
mkdir -p deploy

# Create a directory for documentation
mkdir -p docs

# Create initial files
touch app/main.py
touch app/models/__init__.py
touch app/routers/__init__.py
touch app/utils/__init__.py
touch config/config.yaml
touch tests/__init__.py
touch deploy/Dockerfile
touch deploy/docker-compose.yml
touch README.md
touch .gitignore

echo "Basic directory structure for FastAPI model serving app created successfully."