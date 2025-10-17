#!/bin/bash
# Startup script for the Smart Resume Screener frontend

echo "Starting Smart Resume Screener Frontend..."
echo "========================================="

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing Node.js dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Start the frontend
echo "Starting React development server..."
cd frontend
npm start
