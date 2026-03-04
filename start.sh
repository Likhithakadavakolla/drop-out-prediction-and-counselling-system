#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Dropout Prediction System...${NC}"

# Kill any existing processes on ports 8000 and 3000
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

# Activate virtual environment and start backend
echo -e "${GREEN}Starting Backend on port 8000...${NC}"
source .venv-1/bin/activate
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 2

# Start frontend
echo -e "${GREEN}Starting Frontend on port 3000...${NC}"
cd frontend-react
npm start &
FRONTEND_PID=$!
cd ..

echo -e "${BLUE}Both servers are starting...${NC}"
echo -e "${GREEN}Backend: http://localhost:8000${NC}"
echo -e "${GREEN}Frontend: http://localhost:3000${NC}"
echo -e "Press Ctrl+C to stop both servers"

# Wait for user interrupt
wait
