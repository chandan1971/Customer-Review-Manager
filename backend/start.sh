#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Read host and port from environment variables
HOST=${HOST:-127.0.0.1}
PORT=${PORT:-8000}

# Run the API
uvicorn app.main:app --reload --host $HOST --port $PORT
