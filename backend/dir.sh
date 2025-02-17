#!/bin/bash

# Define project root
PROJECT_ROOT="backend"

# Create main project directory
mkdir -p $PROJECT_ROOT

# Create core FastAPI directories
mkdir -p $PROJECT_ROOT/app/{api,models,schemas,services,ml_models,database,core,utils}

# Create test directory
mkdir -p $PROJECT_ROOT/tests

# Create main FastAPI files
touch $PROJECT_ROOT/app/main.py
touch $PROJECT_ROOT/app/__init__.py

# API routes
touch $PROJECT_ROOT/app/api/{auth.py,users.py,multimodal.py,__init__.py}

# Database setup
touch $PROJECT_ROOT/app/database/{session.py,init_db.py,__init__.py}

# Models (SQLAlchemy)
touch $PROJECT_ROOT/app/models/{user.py,multimodal.py,__init__.py}

# Pydantic Schemas
touch $PROJECT_ROOT/app/schemas/{user.py,multimodal.py,__init__.py}

# Services (Business logic)
touch $PROJECT_ROOT/app/services/{auth_service.py,multimodal_service.py,__init__.py}

# ML Models
touch $PROJECT_ROOT/app/ml_models/{image_model.py,audio_model.py,video_model.py,preprocess.py,__init__.py}

# Core configurations
touch $PROJECT_ROOT/app/core/{config.py,security.py,__init__.py}

# Utility scripts
touch $PROJECT_ROOT/app/utils/{file_utils.py,ml_utils.py,__init__.py}

# Other important files
touch $PROJECT_ROOT/tests/__init__.py
touch $PROJECT_ROOT/requirements.txt
touch $PROJECT_ROOT/Dockerfile
# touch $PROJECT_ROOT/.env

# Display success message
echo "FastAPI backend directory structure completed!"
