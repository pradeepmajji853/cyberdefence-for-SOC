#!/bin/bash

# Cyber Defense Assistant - Demo Startup Script
echo "🛡️ Starting Cyber Defense Assistant Demo..."
echo "==============================================="

# Check if we're in the right directory
if [[ ! -f "main.py" ]]; then
    echo "❌ Error: Please run this script from the cyber defence directory"
    exit 1
fi

# Create .env file if it doesn't exist
if [[ ! -f ".env" ]]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️ Please edit .env file and add your OpenAI API key!"
    echo "   OPENAI_API_KEY=your_key_here"
    read -p "Press Enter after you've added your OpenAI API key to .env..."
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "🎯 Setup complete!"
echo ""
echo "To start the demo:"
echo "1. Terminal 1 - Backend API:"
echo "   python main.py"
echo ""
echo "2. Terminal 2 - Frontend:"
echo "   cd frontend && npm start"
echo ""
echo "3. Terminal 3 - Generate fake logs:"
echo "   python fake_log_generator.py"
echo ""
echo "4. Open browser: http://localhost:3000"
echo ""
echo "🚀 Happy hacking!"
