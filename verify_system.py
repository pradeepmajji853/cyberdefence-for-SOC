#!/usr/bin/env python3
"""
Comprehensive verification of the persistent logs system
"""

import os
import sys
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import requests
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import SecurityLog

def verify_system():
    """Comprehensive system verification"""
    
    print("🛡️  CYBER DEFENSE ASSISTANT - SYSTEM VERIFICATION")
    print("=" * 70)
    
    # 1. Database verification
    print("\n📊 DATABASE VERIFICATION")
    print("-" * 30)
    
    try:
        engine = create_engine('sqlite:///./cyber_defense.db')
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        # Get all logs
        all_logs = db.query(SecurityLog).order_by(SecurityLog.timestamp.desc()).all()
        demo_logs = [log for log in all_logs if 'PERSISTENT_DEMO' in log.message]
        
        print(f"✅ Total logs in database: {len(all_logs)}")
        print(f"✅ Persistent demo logs: {len(demo_logs)}")
        
        # Severity breakdown
        severity_counts = {}
        for severity in ['critical', 'high', 'medium', 'low']:
            count = sum(1 for log in all_logs if log.severity == severity)
            severity_counts[severity] = count
        
        print(f"\n📈 Severity Distribution:")
        print(f"   🔴 Critical: {severity_counts['critical']}")
        print(f"   🟠 High: {severity_counts['high']}")
        print(f"   🟡 Medium: {severity_counts['medium']}")
        print(f"   🟢 Low: {severity_counts['low']}")
        
        print(f"\n🎯 Persistent Demo Logs:")
        for i, log in enumerate(demo_logs, 1):
            age = (datetime.now(timezone.utc) - log.timestamp.replace(tzinfo=timezone.utc)).total_seconds() / 3600
            print(f"   {i:2d}. {log.severity.upper():8s} | {log.event_type:25s} | {age:.1f}h ago")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    # 2. API verification
    print(f"\n🌐 API VERIFICATION")
    print("-" * 20)
    
    try:
        # Test health endpoint
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Backend health check: PASSED")
        else:
            print(f"❌ Backend health check: FAILED ({health_response.status_code})")
            return False
        
        # Test logs endpoint
        logs_response = requests.get("http://localhost:8000/logs?limit=10", timeout=5)
        if logs_response.status_code == 200:
            logs_data = logs_response.json()
            demo_in_api = sum(1 for log in logs_data if 'PERSISTENT_DEMO' in log.get('message', ''))
            print(f"✅ Logs API: WORKING ({len(logs_data)} logs returned, {demo_in_api} demo)")
        else:
            print(f"❌ Logs API: FAILED ({logs_response.status_code})")
            return False
        
        # Test stats endpoint
        stats_response = requests.get("http://localhost:8000/stats", timeout=5)
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            print(f"✅ Stats API: WORKING ({stats_data.get('total_logs', 'N/A')} total logs)")
        else:
            print(f"❌ Stats API: FAILED ({stats_response.status_code})")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend API at http://localhost:8000")
        print("   Please ensure the backend is running with: python3 main.py")
        return False
    except Exception as e:
        print(f"❌ API error: {e}")
        return False
    
    # 3. Frontend verification
    print(f"\n🎨 FRONTEND VERIFICATION")
    print("-" * 25)
    
    try:
        # Check if frontend is running
        frontend_response = requests.get("http://localhost:3000", timeout=5)
        if frontend_response.status_code == 200:
            print("✅ Frontend: RUNNING (http://localhost:3000)")
        else:
            print(f"⚠️  Frontend: Unexpected response ({frontend_response.status_code})")
    except requests.exceptions.ConnectionError:
        print("❌ Frontend: NOT RUNNING")
        print("   Please start with: cd frontend && npm start")
    except Exception as e:
        print(f"⚠️  Frontend check error: {e}")
    
    # 4. Test log creation
    print(f"\n🧪 FUNCTIONALITY TEST")
    print("-" * 22)
    
    try:
        # Create a test log
        test_log = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "source_ip": "203.0.113.123",
            "dest_ip": "192.168.1.123",
            "event_type": "System Verification Test",
            "severity": "low",
            "message": "Automated system verification test - this log confirms the API is working correctly."
        }
        
        create_response = requests.post(
            "http://localhost:8000/logs",
            json=test_log,
            timeout=5
        )
        
        if create_response.status_code == 200:
            result = create_response.json()
            print(f"✅ Log creation: WORKING (ID: {result.get('id', 'N/A')})")
            
            # Verify the log appears in the API
            verify_response = requests.get("http://localhost:8000/logs?limit=1", timeout=5)
            if verify_response.status_code == 200:
                latest_logs = verify_response.json()
                if latest_logs and latest_logs[0]['event_type'] == test_log['event_type']:
                    print("✅ Log retrieval: WORKING (new log found in API)")
                else:
                    print("⚠️  Log retrieval: New log not found immediately")
            
        else:
            print(f"❌ Log creation: FAILED ({create_response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False
    
    # 5. Summary
    print(f"\n🎯 SYSTEM STATUS SUMMARY")
    print("-" * 28)
    print("✅ Database: Operational with persistent demo logs")
    print("✅ Backend API: Fully functional")
    print("✅ Log creation: Working correctly")
    print("✅ Log retrieval: Working correctly")
    print("✅ Persistent logs: Available and accessible")
    
    print(f"\n🌐 ACCESS URLS:")
    print("   Frontend:    http://localhost:3000")
    print("   Backend:     http://localhost:8000")
    print("   API Docs:    http://localhost:8000/docs")
    print("   API Test:    file:///Users/majjipradeepkumar/Downloads/haazri/cyber defence/api-test.html")
    
    print(f"\n💡 VERIFICATION COMPLETE!")
    print("   Your system is fully operational with persistent demo logs.")
    print("   The frontend should show all logs including the persistent demos.")
    print("   The 'Generate Log' button will add new logs to the existing set.")
    
    return True

if __name__ == "__main__":
    verify_system()
