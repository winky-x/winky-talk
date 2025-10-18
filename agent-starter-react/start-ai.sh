#!/bin/bash

echo "🚀 Starting AI Assistant..."

# Start backend first
echo "Starting Python backend..."
cd ../Jarvis_code
source venv/bin/activate
PYTHONUNBUFFERED=1 python -O agent.py dev &
BACKEND_PID=$!

# Wait for backend to initialize
echo "Waiting for backend to start..."
sleep 8

# Start frontend
echo "Starting React frontend..."
cd ../agent-starter-react
pnpm next:dev &
FRONTEND_PID=$!

echo "✅ Both services started!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Frontend URL: http://localhost:3001"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for user interrupt
wait