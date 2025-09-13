#!/bin/bash

# Cyber Defense Assistant - Complete Demo Script
# This script demonstrates all features of the AI-powered SOC system

echo "🛡️  CYBER DEFENSE ASSISTANT DEMO"
echo "=================================="
echo ""

# Function to check if a service is running
check_service() {
    local port=$1
    local service=$2
    if curl -s http://localhost:$port/health > /dev/null 2>&1; then
        echo "✅ $service is running on port $port"
        return 0
    else
        echo "❌ $service is not running on port $port"
        return 1
    fi
}

# Function to show API endpoints
demo_api() {
    echo ""
    echo "📊 TESTING API ENDPOINTS"
    echo "========================"
    
    echo ""
    echo "1. Health Check:"
    curl -s http://localhost:8000/health | jq '.'
    
    echo ""
    echo "2. Recent Logs (5 entries):"
    curl -s "http://localhost:8000/logs?limit=5" | jq '.[0:2]'
    
    echo ""
    echo "3. Statistics:"
    curl -s http://localhost:8000/stats | jq '.'
    
    echo ""
    echo "4. AI Analysis:"
    curl -s http://localhost:8000/analysis | jq '.summary'
    
    echo ""
}

# Function to simulate live attack
demo_live_attack() {
    echo ""
    echo "🚨 SIMULATING LIVE CYBER ATTACK"
    echo "==============================="
    
    echo "Generating realistic attack scenarios..."
    python3 -c "
from fake_log_generator import generate_brute_force_logs, generate_malware_logs
import requests
import time

# Generate brute force attack
logs = generate_brute_force_logs(1)
for log in logs:
    try:
        response = requests.post('http://localhost:8000/logs', json=log)
        print(f'✅ Brute Force Event: {log[\"event_type\"]} - {log[\"severity\"]}')
    except Exception as e:
        print(f'❌ Failed to log event: {e}')
    time.sleep(0.5)

# Generate malware detection
logs = generate_malware_logs(1)
for log in logs:
    try:
        response = requests.post('http://localhost:8000/logs', json=log)
        print(f'✅ Malware Event: {log[\"event_type\"]} - {log[\"severity\"]}')
    except Exception as e:
        print(f'❌ Failed to log event: {e}')
    time.sleep(0.5)

print('\\n🔄 Attack simulation complete. Check the dashboard for updates!')
"
}

# Main demo flow
main() {
    echo "🔍 Checking system status..."
    
    # Check backend
    if check_service 8000 "Backend API"; then
        echo "✅ Backend is operational"
    else
        echo "❌ Please start the backend: python3 main.py"
        exit 1
    fi
    
    # Check frontend
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ Frontend is operational"
    else
        echo "❌ Please start the frontend: cd frontend && npm start"
        exit 1
    fi
    
    # Demo API functionality
    demo_api
    
    # Demo live attack simulation
    demo_live_attack
    
    echo ""
    echo "🎯 DEMO COMPLETE!"
    echo "=================="
    echo ""
    echo "🌐 Frontend Dashboard: http://localhost:3000"
    echo "🔧 API Documentation: http://localhost:8000/docs"
    echo "🧪 API Test Page: http://localhost:3000/api-test.html"
    echo ""
    echo "📋 Key Features Demonstrated:"
    echo "   • Real-time security log ingestion"
    echo "   • AI-powered threat analysis" 
    echo "   • Interactive dashboard with military SOC theme"
    echo "   • Live attack simulation"
    echo "   • RESTful API with 7 endpoints"
    echo ""
    echo "🚀 For presentation mode, run: python3 live_demo.py"
    echo "📚 For detailed guide, see: DEMO_GUIDE.md"
}

# Run the demo
main
