#!/bin/bash

# Activate the virtual environment
source /var/www/backend/AIron/venv/bin/activate

# Change to the directory containing the API
cd /var/www/backend/AIron/AIron-API

# Add the API directory to the Python path
export PYTHONPATH=/var/www/backend/AIron/AIron-API:$PYTHONPATH

# Start the API
uvicorn main:app --host 0.0.0.0 --port 8000
