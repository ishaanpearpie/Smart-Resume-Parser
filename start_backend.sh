#!/bin/bash
# Startup script for the Smart Resume Screener backend

echo "Starting Smart Resume Screener Backend..."
echo "========================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/pyvenv.cfg" ] || ! pip list | grep -q fastapi; then
    echo "Installing Python dependencies..."
    cd backend
    pip install -r requirements.txt
    cd ..
fi

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "Warning: .env file not found in backend directory"
    echo "Please create backend/.env with your GOOGLE_API_KEY"
    echo "You can copy from backend/env.example"
    exit 1
fi

# Start the backend
echo "Starting FastAPI server..."
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
