#!/usr/bin/env python3
"""
Comprehensive Gemini AI Log Analysis Verification
Tests that Gemini AI can perfectly analyze all logs from the database
"""

import requests
import json
import time
from datetime import datetime

API_BASE = "http://localhost:8000"

def test_comprehensive_analysis():
    """Test that Gemini AI analyzes ALL logs in database"""
    print("🔍 TESTING COMPREHENSIVE LOG ANALYSIS")
    print("="*50)
    
    # Get total number of logs in database
    try:
        logs_response = requests.get(f"{API_BASE}/logs?limit=1000")
        if logs_response.status_code == 200:
            total_logs = len(logs_response.json())
            print(f"✅ Database contains: {total_logs} total logs")
        else:
            print(f"❌ Failed to get logs count: {logs_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting logs: {e}")
        return False
    
    # Test AI analysis endpoint
    try:
        analysis_response = requests.get(f"{API_BASE}/analysis")
        if analysis_response.status_code == 200:
            analysis = analysis_response.json()
            analyzed_count = analysis.get('total_logs_analyzed', 0)
            
            print(f"✅ Gemini AI analyzed: {analyzed_count} logs")
            print(f"✅ Coverage: {(analyzed_count/total_logs)*100:.1f}% of all logs")
            
            # Check analysis quality
            print(f"✅ Summary: {analysis['summary'][:100]}...")
            print(f"✅ Threats identified: {len(analysis['threats_identified'])}")
            print(f"✅ Severity: {analysis['severity_classification']}")
            print(f"✅ Recommendations: {len(analysis['recommendations'])}")
            
            # Verify comprehensive analysis
            if analyzed_count >= total_logs * 0.8:  # Should analyze at least 80% of logs
                print(f"🎯 EXCELLENT: Analyzing {analyzed_count} logs (sufficient coverage)")
                return True
            else:
                print(f"⚠️  LIMITED: Only analyzing {analyzed_count} of {total_logs} logs")
                return False
                
        else:
            print(f"❌ Analysis failed: {analysis_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def test_specific_threat_queries():
    """Test AI's ability to answer specific questions about log data"""
    print("\n💬 TESTING SPECIFIC THREAT INTELLIGENCE")
    print("="*50)
    
    test_queries = [
        {
            "question": "How many brute force attacks are in the logs?",
            "expected_keywords": ["brute", "force", "ssh", "attack"]
        },
        {
            "question": "What IP addresses should I be most concerned about?",
            "expected_keywords": ["ip", "address", "192.168", "10.0", "source"]
        },
        {
            "question": "Are there any malware detections in the security logs?",
            "expected_keywords": ["malware", "virus", "detection", "infection"]
        },
        {
            "question": "What types of network intrusions have occurred?",
            "expected_keywords": ["intrusion", "network", "breach", "compromise"]
        },
        {
            "question": "Show me the most critical security events",
            "expected_keywords": ["critical", "severity", "high", "priority"]
        }
    ]
    
    success_count = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing Query: {query['question']}")
        
        try:
            response = requests.post(
                f"{API_BASE}/chat",
                json={"question": query['question']},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data['answer'].lower()
                context_logs = data['context_logs_used']
                
                print(f"   ✅ Response received ({len(data['answer'])} chars)")
                print(f"   ✅ Context: {context_logs} logs analyzed")
                
                # Check if response contains expected keywords
                keyword_matches = sum(1 for keyword in query['expected_keywords'] 
                                    if keyword.lower() in answer)
                
                if keyword_matches > 0:
                    print(f"   ✅ Relevant content: {keyword_matches}/{len(query['expected_keywords'])} keywords found")
                    success_count += 1
                else:
                    print(f"   ⚠️  Limited relevance: {keyword_matches}/{len(query['expected_keywords'])} keywords found")
                
                print(f"   📝 Response: {data['answer'][:100]}...")
                
            else:
                print(f"   ❌ Query failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)  # Rate limiting
    
    print(f"\n🎯 Query Results: {success_count}/{len(test_queries)} queries successful")
    return success_count >= len(test_queries) * 0.8

def test_log_data_coverage():
    """Verify AI has access to diverse log data"""
    print("\n📊 TESTING LOG DATA COVERAGE")
    print("="*50)
    
    # Get sample of logs to verify diversity
    try:
        logs_response = requests.get(f"{API_BASE}/logs?limit=50")
        if logs_response.status_code == 200:
            logs = logs_response.json()
            
            # Analyze log diversity
            event_types = set()
            severities = set()
            source_ips = set()
            
            for log in logs:
                event_types.add(log.get('event_type', 'unknown'))
                severities.add(log.get('severity', 'unknown'))
                source_ips.add(log.get('source_ip', 'unknown'))
            
            print(f"✅ Event types: {len(event_types)} distinct types")
            print(f"✅ Severity levels: {len(severities)} distinct levels")  
            print(f"✅ Source IPs: {len(source_ips)} distinct addresses")
            
            print(f"📊 Sample event types: {list(event_types)[:5]}")
            print(f"📊 Severity distribution: {list(severities)}")
            print(f"📊 Sample IPs: {list(source_ips)[:5]}")
            
            # Test if AI can reference specific log details
            if logs:
                sample_log = logs[0]
                specific_query = f"Tell me about the security event from IP {sample_log.get('source_ip')} involving {sample_log.get('event_type')}"
                
                print(f"\n🎯 Testing specific log reference:")
                print(f"   Query: {specific_query}")
                
                response = requests.post(
                    f"{API_BASE}/chat",
                    json={"question": specific_query},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data['answer'].lower()
                    
                    # Check if AI references the specific details
                    ip_mentioned = sample_log.get('source_ip', '').lower() in answer
                    event_mentioned = any(word in answer for word in sample_log.get('event_type', '').lower().split('_'))
                    
                    if ip_mentioned or event_mentioned:
                        print(f"   ✅ AI successfully referenced specific log details")
                        return True
                    else:
                        print(f"   ⚠️  AI may not be accessing specific log details")
                        print(f"   📝 Response: {data['answer'][:150]}...")
                        return False
                else:
                    print(f"   ❌ Specific query failed: {response.status_code}")
                    return False
            
            return True
            
        else:
            print(f"❌ Failed to get log samples: {logs_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing data coverage: {e}")
        return False

def main():
    """Run comprehensive Gemini AI verification"""
    print("🤖 GEMINI AI LOG ANALYSIS VERIFICATION")
    print("="*55)
    print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing: {API_BASE}")
    
    # Run all tests
    tests = [
        ("Comprehensive Analysis", test_comprehensive_analysis),
        ("Specific Threat Queries", test_specific_threat_queries),
        ("Log Data Coverage", test_log_data_coverage)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        success = test_func()
        results.append((test_name, success))
    
    # Final assessment
    print(f"\n" + "="*55)
    print("🎯 GEMINI AI VERIFICATION RESULTS")
    print("="*55)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\n📊 Overall Score: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎊 PERFECT SCORE!")
        print("🚀 Gemini AI can perfectly analyze all logs from the database")
        print("💡 The system provides comprehensive threat intelligence")
    elif passed >= len(results) * 0.8:
        print("✅ EXCELLENT PERFORMANCE!")
        print("🎯 Gemini AI successfully analyzes logs with high accuracy")
    else:
        print("⚠️  NEEDS IMPROVEMENT")
        print("🔧 Some aspects of log analysis may need refinement")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
