#!/bin/bash

# Quick demo launcher - runs all components
echo "🛡️ Cyber Defense Assistant - Quick Start"
echo "========================================"

# Check requirements
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install Node.js and npm"
    exit 1
fi

# Create .env if needed
if [[ ! -f ".env" ]]; then
    echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
    echo "⚠️ Created .env file. Please add your OpenAI API key!"
    echo "Edit .env and add: OPENAI_API_KEY=your_actual_key"
fi

echo "🚀 Starting demo components..."

# Start backend in background
echo "Starting backend server..."
python main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Install frontend deps if needed
if [[ ! -d "frontend/node_modules" ]]; then
    echo "Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

# Start frontend in background
echo "Starting frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎯 Demo is starting!"
echo "Backend API: http://localhost:8000"
echo "Frontend: http://localhost:3000 (will open automatically)"
echo ""
echo "To generate fake logs, run in another terminal:"
echo "python fake_log_generator.py"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT
wait
