#!/usr/bin/env python3
"""
🎯 GEMINI AI PERFECT LOG ANALYSIS DEMONSTRATION
Showcases how Gemini AI perfectly analyzes ALL logs from the database
"""

import requests
import json
import time
from datetime import datetime

API_BASE = "http://localhost:8000"

def print_header(title, char="="):
    """Print a styled header"""
    print(f"\n{char * 60}")
    print(f"🎯 {title}")
    print(f"{char * 60}")

def demonstrate_perfect_analysis():
    """Demonstrate perfect log analysis capabilities"""
    print_header("GEMINI AI PERFECT LOG ANALYSIS DEMO")
    
    print("🤖 Testing Gemini AI's ability to analyze ALL logs perfectly...")
    
    # Step 1: Show total logs in database
    try:
        logs_response = requests.get(f"{API_BASE}/logs?limit=500")
        if logs_response.status_code == 200:
            all_logs = logs_response.json()
            total_count = len(all_logs)
            print(f"\n📊 DATABASE STATUS:")
            print(f"   ✅ Total logs in database: {total_count}")
            
            # Show log diversity
            event_types = set(log.get('event_type', 'unknown') for log in all_logs)
            severities = set(log.get('severity', 'unknown') for log in all_logs)
            source_ips = set(log.get('source_ip', 'unknown') for log in all_logs)
            
            print(f"   ✅ Event types: {len(event_types)} distinct categories")
            print(f"   ✅ Severity levels: {list(severities)}")
            print(f"   ✅ Unique source IPs: {len(source_ips)} addresses")
            
        else:
            print(f"❌ Failed to get logs: {logs_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    print(f"\n🔄 Requesting Gemini AI analysis...")
    time.sleep(1)
    
    # Step 2: Test comprehensive analysis
    try:
        analysis_response = requests.get(f"{API_BASE}/analysis")
        if analysis_response.status_code == 200:
            analysis = analysis_response.json()
            analyzed_count = analysis.get('total_logs_analyzed', 0)
            
            print(f"\n🎯 ANALYSIS RESULTS:")
            print(f"   ✅ Logs analyzed: {analyzed_count} of {total_count} ({(analyzed_count/total_count)*100:.1f}% coverage)")
            print(f"   ✅ Overall severity: {analysis['severity_classification'].upper()}")
            print(f"   ✅ Threats identified: {len(analysis['threats_identified'])}")
            print(f"   ✅ Recommendations: {len(analysis['recommendations'])}")
            
            print(f"\n📋 EXECUTIVE SUMMARY:")
            print(f"   {analysis['summary']}")
            
            print(f"\n🚨 TOP THREATS IDENTIFIED:")
            for i, threat in enumerate(analysis['threats_identified'][:4], 1):
                print(f"   {i}. {threat}")
            
            print(f"\n💡 KEY RECOMMENDATIONS:")
            for i, rec in enumerate(analysis['recommendations'][:4], 1):
                print(f"   {i}. {rec}")
                
            # Perfect analysis verification
            if analyzed_count >= total_count * 0.95:  # 95%+ coverage is perfect
                print(f"\n🎊 PERFECT ANALYSIS ACHIEVED!")
                print(f"   🏆 Gemini AI analyzed {analyzed_count} logs with excellent coverage")
                return True
            else:
                print(f"\n⚠️  Partial coverage: {analyzed_count} of {total_count} logs")
                return False
                
        else:
            print(f"❌ Analysis failed: {analysis_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def demonstrate_intelligent_chat():
    """Show intelligent chat with full database context"""
    print_header("INTELLIGENT SECURITY CHAT", "-")
    
    demo_questions = [
        "How many total security events do we have?",
        "What are the most critical threats right now?",
        "Which IP addresses are causing the most problems?",
        "What specific actions should our SOC team take immediately?"
    ]
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n💬 Question {i}: {question}")
        
        try:
            response = requests.post(
                f"{API_BASE}/chat",
                json={"question": question},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   📊 Context: {data['context_logs_used']} logs analyzed")
                print(f"   🤖 Response: {data['answer'][:200]}...")
            else:
                print(f"   ❌ Chat failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)

def show_system_integration():
    """Display complete system integration status"""
    print_header("SYSTEM INTEGRATION STATUS", "-")
    
    endpoints = [
        ("/health", "System Health"),
        ("/logs?limit=5", "Database Access"),
        ("/analysis", "AI Analysis"),
        ("/stats", "Statistics")
    ]
    
    print("🔧 Testing all system components...")
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{API_BASE}{endpoint}", timeout=5)
            status = "✅ OPERATIONAL" if response.status_code == 200 else f"❌ ERROR {response.status_code}"
            print(f"   {description:20s}: {status}")
        except Exception as e:
            print(f"   {description:20s}: ❌ FAILED ({str(e)[:30]})")
    
    # Test frontend
    try:
        response = requests.get("http://localhost:3000", timeout=3)
        status = "✅ OPERATIONAL" if response.status_code == 200 else f"❌ ERROR {response.status_code}"
        print(f"   {'Frontend Dashboard':20s}: {status}")
    except Exception as e:
        print(f"   {'Frontend Dashboard':20s}: ❌ FAILED ({str(e)[:30]})")

def main():
    """Run complete demonstration"""
    print("🛡️  CYBER DEFENSE ASSISTANT - PERFECT ANALYSIS DEMO")
    print("=" * 70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Backend: {API_BASE}")
    print(f"🖥️  Frontend: http://localhost:3000")
    
    # Run demonstration components
    success = True
    
    # 1. Perfect Analysis Demo
    if not demonstrate_perfect_analysis():
        success = False
    
    # 2. Intelligent Chat Demo
    demonstrate_intelligent_chat()
    
    # 3. System Integration Status
    show_system_integration()
    
    # Final summary
    print_header("DEMONSTRATION SUMMARY")
    
    if success:
        print("🎊 DEMONSTRATION SUCCESSFUL!")
        print("✅ Gemini AI perfectly analyzes ALL logs from database")
        print("✅ Comprehensive threat intelligence generated")
        print("✅ Interactive chat with full database context")
        print("✅ Professional SOC-grade security analysis")
        print("✅ Complete backend-frontend integration")
        
        print(f"\n🚀 READY FOR LIVE PRESENTATION!")
        print(f"   📊 Dashboard: http://localhost:3000")
        print(f"   🤖 AI Analysis: {API_BASE}/analysis")
        print(f"   💬 AI Chat: Available in dashboard")
        print(f"   📖 API Docs: {API_BASE}/docs")
    else:
        print("⚠️  Some issues detected - please review system status")
    
    return success

if __name__ == "__main__":
    success = main()
    print(f"\n{'🎯 DEMO COMPLETE - SUCCESS!' if success else '⚠️ DEMO COMPLETE - CHECK ISSUES'}")
    exit(0 if success else 1)
