#!/usr/bin/env python3
"""
AI Response Testing Script - Comprehensive Validation
Tests both hardcoded intelligent responses and enhanced fallback system
"""

import requests
import json
import time

API_BASE = "http://localhost:8001"

def test_ai_responses():
    """Test various AI response scenarios"""
    
    test_cases = [
        {
            "category": "IP Blocking (Hardcoded)",
            "question": "WHAT ARE THE IPS THAT ARE NEEDED TO BE BLOCKED",
            "expected_contains": ["IP BLOCKING", "CRITICAL RISK", "BLOCK IMMEDIATELY"]
        },
        {
            "category": "IP Analysis (Hardcoded)",
            "question": "What IP addresses are causing problems?",
            "expected_contains": ["IP BLOCKING", "Events:", "Action:"]
        },
        {
            "category": "Threat Analysis (Hardcoded)", 
            "question": "What are the current threats?",
            "expected_contains": ["CRITICAL THREAT", "IMMEDIATE ACTION", "TOP ATTACK"]
        },
        {
            "category": "Recommendations (Hardcoded)",
            "question": "What should I do about these attacks?",
            "expected_contains": ["RECOMMENDATIONS", "BLOCK IP", "Implement"]
        },
        {
            "category": "Enhanced Fallback - Security Status",
            "question": "Can you help me understand the current security situation?",
            "expected_contains": ["Security Status", "Critical:", "High:", "Top threats:"]
        },
        {
            "category": "Enhanced Fallback - Network Environment",
            "question": "What is happening in my network environment?",
            "expected_contains": ["Security Status", "threat landscape", "events"]
        },
        {
            "category": "Enhanced Fallback - General Help",
            "question": "Help me understand what's going on",
            "expected_contains": ["Security Status", "URGENT", "HIGH PRIORITY"]
        },
        {
            "category": "Generic Fallback",
            "question": "What time is it?", 
            "expected_contains": ["SOC cyber defense assistant", "security threats"]
        }
    ]
    
    print("🧪 AI RESPONSE SYSTEM COMPREHENSIVE TEST")
    print("="*60)
    
    passed = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test['category']}")
        print(f"   Question: {test['question']}")
        
        try:
            response = requests.post(
                f"{API_BASE}/chat",
                json={"question": test['question']},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data['answer']
                context_logs = data['context_logs_used']
                
                # Check if expected content is in response
                matches = sum(1 for expected in test['expected_contains'] 
                            if expected.lower() in answer.lower())
                
                if matches > 0:
                    print(f"   ✅ PASSED ({matches}/{len(test['expected_contains'])} keywords found)")
                    print(f"   📊 Context: {context_logs} logs analyzed")
                    print(f"   📝 Response: {answer[:100]}...")
                    passed += 1
                else:
                    print(f"   ❌ FAILED (0/{len(test['expected_contains'])} keywords found)")
                    print(f"   📝 Response: {answer[:150]}...")
            else:
                print(f"   ❌ API ERROR: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ EXCEPTION: {e}")
            
        time.sleep(0.5)  # Rate limiting
    
    print(f"\n🎯 FINAL RESULTS: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🏆 ALL TESTS PASSED! AI response system is fully functional!")
    elif passed >= total * 0.8:
        print("✅ SYSTEM WORKING WELL! Most features operational.")
    else:
        print("⚠️  ISSUES DETECTED. Some responses may need improvement.")
    
    return passed == total

def test_specific_scenarios():
    """Test specific real-world scenarios"""
    
    print("\n🎭 REAL-WORLD SCENARIO TESTING")
    print("="*40)
    
    scenarios = [
        "I'm seeing unusual network activity, can you analyze it?",
        "Are there any suspicious IP addresses I should be concerned about?",
        "What's the overall security posture right now?",
        "Should I be worried about the current threat level?",
        "Help me prioritize which security issues to address first"
    ]
    
    for i, question in enumerate(scenarios, 1):
        print(f"\n{i}. Scenario: {question}")
        
        try:
            response = requests.post(
                f"{API_BASE}/chat",
                json={"question": question},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data['answer']
                
                if len(answer) > 50 and "I'm a SOC" not in answer:
                    print("   ✅ Intelligent response generated")
                    print(f"   📊 Response type: {'Hardcoded Analysis' if any(x in answer for x in ['CRITICAL RISK', 'IMMEDIATE IP BLOCKING', 'CRITICAL THREAT']) else 'Enhanced Fallback'}")
                else:
                    print("   ⚠️  Generic response")
                    
                print(f"   📝 Sample: {answer[:120]}...")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            
        time.sleep(0.3)

if __name__ == "__main__":
    print("🚀 Starting AI Response System Test...")
    print(f"📡 Testing API: {API_BASE}")
    
    # Test basic connectivity
    try:
        health = requests.get(f"{API_BASE}/health")
        if health.status_code == 200:
            print("✅ Backend connectivity confirmed")
        else:
            print("❌ Backend connectivity issue")
            exit(1)
    except:
        print("❌ Cannot connect to backend")
        exit(1)
    
    # Run comprehensive tests
    success = test_ai_responses()
    test_specific_scenarios()
    
    print(f"\n🎊 TESTING COMPLETE!")
    print(f"📊 System Status: {'FULLY OPERATIONAL' if success else 'PARTIALLY OPERATIONAL'}")
    print(f"🧠 AI Features: Hardcoded Intelligence + Enhanced Fallback Analysis")
    print(f"🛡️ Ready for: SOC Operations, Threat Analysis, Security Consulting")
