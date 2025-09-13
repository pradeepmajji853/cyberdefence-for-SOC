#!/usr/bin/env python3
"""
Gemini AI Demo Script for Cyber Defense Assistant
Demonstrates the AI-powered threat analysis and chat capabilities
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_gemini_analysis():
    """Test Gemini AI threat analysis"""
    print("🔍 Testing Gemini AI Threat Analysis...")
    
    response = requests.get(f"{API_BASE}/analysis")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Analysis Summary: {data['summary'][:100]}...")
        print(f"🎯 Threats Found: {len(data['threats_identified'])} threats")
        print(f"⚠️  Severity: {data['severity_classification'].upper()}")
        print(f"📊 Logs Analyzed: {data['total_logs_analyzed']}")
        return True
    else:
        print(f"❌ Analysis failed: {response.status_code}")
        return False

def test_gemini_chat():
    """Test Gemini AI chat interface"""
    print("\n💬 Testing Gemini AI Chat Interface...")
    
    questions = [
        "What are the most critical threats right now?",
        "Should I be worried about any specific IP addresses?", 
        "What's the most common attack type in our logs?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. Q: {question}")
        
        response = requests.post(
            f"{API_BASE}/chat",
            json={"question": question},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data['answer'][:200] + "..." if len(data['answer']) > 200 else data['answer']
            print(f"   A: {answer}")
        else:
            print(f"   ❌ Chat failed: {response.status_code}")
        
        time.sleep(1)  # Rate limiting

def test_system_health():
    """Test overall system health"""
    print("\n🏥 System Health Check...")
    
    # Test health endpoint
    response = requests.get(f"{API_BASE}/health")
    if response.status_code == 200:
        print("✅ Backend API: Healthy")
    else:
        print("❌ Backend API: Unhealthy")
        return False
    
    # Test stats
    response = requests.get(f"{API_BASE}/stats")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Database: {data['total_logs']} security events")
        print(f"✅ Critical Events: {data['last_24h_severity']['critical']}")
        print(f"✅ High Severity: {data['last_24h_severity']['high']}")
    else:
        print("❌ Stats endpoint failed")
        return False
    
    return True

def main():
    """Run complete Gemini AI demo"""
    print("🛡️  GEMINI AI CYBER DEFENSE DEMO")
    print("=" * 40)
    
    # Health check first
    if not test_system_health():
        print("\n❌ System health check failed. Please ensure backend is running.")
        return
    
    # Test AI analysis
    if not test_gemini_analysis():
        print("\n❌ AI analysis test failed.")
        return
    
    # Test AI chat
    test_gemini_chat()
    
    print("\n" + "=" * 40)
    print("🎉 GEMINI AI DEMO COMPLETE!")
    print("\nKey Features Demonstrated:")
    print("• AI-powered threat analysis with specific recommendations")
    print("• Natural language security chat with contextual responses")
    print("• Real-time processing of 150+ security events")
    print("• Military SOC-grade intelligence and insights")
    print(f"\n🌐 Dashboard: http://localhost:3000")
    print(f"🔧 API Docs: {API_BASE}/docs")

if __name__ == "__main__":
    main()
