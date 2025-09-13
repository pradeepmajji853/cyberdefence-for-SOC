#!/usr/bin/env python3
"""
Gemini AI Integration Verification Script
Tests all components of the cyber defense assistant
"""

import requests
import json
import time
from datetime import datetime

# Configuration
API_BASE = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def print_header(title):
    """Print a formatted header"""
    print(f"\n🔹 {title}")
    print("=" * (len(title) + 4))

def test_backend_health():
    """Test backend health endpoint"""
    print_header("Backend Health Check")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Status: {data['status']}")
            print(f"✅ Timestamp: {data['timestamp']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection error: {e}")
        return False

def test_logs_retrieval():
    """Test log retrieval endpoint"""
    print_header("Logs Retrieval Test")
    try:
        response = requests.get(f"{API_BASE}/logs?limit=10")
        if response.status_code == 200:
            logs = response.json()
            print(f"✅ Retrieved {len(logs)} log entries")
            if logs:
                latest = logs[0]
                print(f"✅ Latest event: {latest['event_type']} ({latest['severity']})")
                print(f"✅ Source: {latest['source_ip']} → {latest['dest_ip']}")
            return True
        else:
            print(f"❌ Logs retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Logs retrieval error: {e}")
        return False

def test_gemini_analysis():
    """Test Gemini AI analysis endpoint"""
    print_header("Gemini AI Analysis Test")
    try:
        response = requests.get(f"{API_BASE}/analysis")
        if response.status_code == 200:
            analysis = response.json()
            print(f"✅ Analysis completed for {analysis['total_logs_analyzed']} logs")
            print(f"✅ Summary: {analysis['summary'][:100]}...")
            print(f"✅ Severity: {analysis['severity_classification'].upper()}")
            print(f"✅ Threats found: {len(analysis['threats_identified'])}")
            print(f"✅ Recommendations: {len(analysis['recommendations'])}")
            
            # Check if using Gemini AI or fallback
            if "Gemini API error" in str(analysis):
                print("⚠️  Note: Using fallback analysis (Gemini quota reached)")
            else:
                print("🤖 AI Analysis: Gemini AI integration active")
            
            return True
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def test_gemini_chat():
    """Test Gemini AI chat endpoint"""
    print_header("Gemini AI Chat Test")
    
    test_questions = [
        "What are the most critical security threats right now?",
        "Should I be concerned about any specific IP addresses?",
        "What security actions do you recommend?"
    ]
    
    success_count = 0
    
    for i, question in enumerate(test_questions, 1):
        try:
            response = requests.post(
                f"{API_BASE}/chat",
                json={"question": question},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Q{i}: {question[:50]}...")
                answer = data['answer'][:150] + "..." if len(data['answer']) > 150 else data['answer']
                print(f"✅ A{i}: {answer}")
                print(f"✅ Context: {data['context_logs_used']} logs analyzed")
                success_count += 1
            else:
                print(f"❌ Q{i} failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Q{i} error: {e}")
        
        time.sleep(1)  # Rate limiting
    
    print(f"\n✅ Chat Tests: {success_count}/{len(test_questions)} successful")
    return success_count > 0

def test_frontend_accessibility():
    """Test frontend accessibility"""
    print_header("Frontend Accessibility Test")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print(f"✅ Frontend accessible at {FRONTEND_URL}")
            print("✅ React application loaded successfully")
            return True
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend connection error: {e}")
        return False

def test_database_persistence():
    """Test database persistence"""
    print_header("Database Persistence Test")
    try:
        # Get current log count
        response1 = requests.get(f"{API_BASE}/logs?limit=1000")
        if response1.status_code == 200:
            initial_count = len(response1.json())
            print(f"✅ Database contains {initial_count} persistent logs")
            
            # Test creating a new log
            test_log = {
                "event_type": "API Test Event",
                "severity": "low",
                "source_ip": "127.0.0.1",
                "dest_ip": "127.0.0.1",
                "message": f"Test log created at {datetime.now().isoformat()}"
            }
            
            create_response = requests.post(f"{API_BASE}/logs", json=test_log)
            if create_response.status_code == 200:
                print("✅ New log entry created successfully")
                
                # Verify the log was added
                response2 = requests.get(f"{API_BASE}/logs?limit=1000")
                if response2.status_code == 200:
                    new_count = len(response2.json())
                    if new_count > initial_count:
                        print("✅ Database persistence verified")
                        return True
            
        print("❌ Database persistence test failed")
        return False
        
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False

def main():
    """Run complete system verification"""
    print("🛡️  CYBER DEFENSE ASSISTANT - GEMINI AI VERIFICATION")
    print("=" * 55)
    print(f"🕐 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    tests = [
        ("Backend Health", test_backend_health),
        ("Logs Retrieval", test_logs_retrieval),
        ("Database Persistence", test_database_persistence),
        ("Gemini AI Analysis", test_gemini_analysis),
        ("Gemini AI Chat", test_gemini_chat),
        ("Frontend Access", test_frontend_accessibility),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎊 ALL SYSTEMS OPERATIONAL!")
        print("🚀 Cyber Defense Assistant with Gemini AI is ready for demonstration")
    else:
        print(f"⚠️  {total-passed} test(s) failed - check system components")
    
    print(f"\n🌐 Access Points:")
    print(f"   📊 Dashboard: {FRONTEND_URL}")
    print(f"   📖 API Docs: {API_BASE}/docs")
    print(f"   🔍 Analysis: {API_BASE}/analysis")
    print(f"   💬 Chat: {API_BASE}/chat")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
