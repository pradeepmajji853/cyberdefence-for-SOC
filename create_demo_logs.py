#!/usr/bin/env python3
"""
Create comprehensive persistent demo logs for the Cyber Defense dashboard
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import SecurityLog, Base

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cyber_defense.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def setup_persistent_demo_data():
    """Create a comprehensive set of demo logs for consistent display"""
    
    db = SessionLocal()
    
    try:
        # Clear existing demo logs to avoid duplicates
        demo_marker = "PERSISTENT_DEMO"
        db.query(SecurityLog).filter(SecurityLog.message.like(f"%{demo_marker}%")).delete()
        
        # Comprehensive demo logs with good variety
        demo_logs_data = [
            # Critical threats (recent)
            {
                "event_type": "Critical System Breach",
                "severity": "critical",
                "source_ip": "203.0.113.45",
                "dest_ip": "192.168.1.100",
                "message": f"Unauthorized root access detected on web server. Multiple authentication bypasses observed. [{demo_marker}]",
                "minutes_ago": 15
            },
            {
                "event_type": "Ransomware Detection",
                "severity": "critical", 
                "source_ip": "192.168.1.65",
                "dest_ip": "192.168.1.0/24",
                "message": f"File encryption activity detected. Ransomware signature matches WannaCry variant. Immediate containment required. [{demo_marker}]",
                "minutes_ago": 45
            },
            {
                "event_type": "Data Exfiltration",
                "severity": "critical",
                "source_ip": "192.168.1.75",
                "dest_ip": "104.244.42.129", 
                "message": f"Large data transfer (2.5GB) to external IP detected. Potential classified data breach in progress. [{demo_marker}]",
                "minutes_ago": 90
            },
            
            # High severity threats
            {
                "event_type": "Advanced Persistent Threat",
                "severity": "high",
                "source_ip": "198.51.100.23",
                "dest_ip": "192.168.1.205",
                "message": f"Sophisticated malware with C2 communication detected. Nation-state actor signatures identified. [{demo_marker}]",
                "minutes_ago": 120
            },
            {
                "event_type": "SQL Injection Attack",
                "severity": "high",
                "source_ip": "93.184.216.34",
                "dest_ip": "192.168.1.100",
                "message": f"Advanced SQL injection targeting military personnel database. 47 injection attempts blocked. [{demo_marker}]",
                "minutes_ago": 180
            },
            {
                "event_type": "Brute Force Attack",
                "severity": "high",
                "source_ip": "45.76.212.198",
                "dest_ip": "192.168.1.50",
                "message": f"Coordinated SSH brute force attack from botnet. 2,847 login attempts in 10 minutes. [{demo_marker}]",
                "minutes_ago": 240
            },
            {
                "event_type": "Insider Threat Alert",
                "severity": "high",
                "source_ip": "192.168.1.85",
                "dest_ip": "192.168.1.220",
                "message": f"Employee accessing classified files outside authorized hours. Behavioral anomaly detected. [{demo_marker}]",
                "minutes_ago": 300
            },
            
            # Medium severity events
            {
                "event_type": "Phishing Campaign",
                "severity": "medium",
                "source_ip": "172.16.254.78",
                "dest_ip": "192.168.1.150",
                "message": f"Sophisticated phishing email bypassed initial filters. Military-themed social engineering detected. [{demo_marker}]",
                "minutes_ago": 360
            },
            {
                "event_type": "Firewall Policy Violation",
                "severity": "medium",
                "source_ip": "10.0.0.45",
                "dest_ip": "192.168.1.200",
                "message": f"Multiple attempts to access restricted ports. Policy violation from internal network. [{demo_marker}]",
                "minutes_ago": 420
            },
            {
                "event_type": "Suspicious Network Traffic",
                "severity": "medium",
                "source_ip": "198.18.0.100",
                "dest_ip": "192.168.1.0/24", 
                "message": f"Network reconnaissance detected. Port scanning across multiple subnets identified. [{demo_marker}]",
                "minutes_ago": 480
            },
            {
                "event_type": "Unauthorized Software Installation",
                "severity": "medium",
                "source_ip": "192.168.1.90",
                "dest_ip": "52.96.128.0",
                "message": f"Installation of unauthorized remote access tool detected on workstation. Policy violation. [{demo_marker}]",
                "minutes_ago": 540
            },
            
            # Low severity (routine events)
            {
                "event_type": "Failed VPN Authentication",
                "severity": "low",
                "source_ip": "203.0.113.99",
                "dest_ip": "192.168.1.1",
                "message": f"VPN authentication failed for user. Standard security protocol activated. [{demo_marker}]",
                "minutes_ago": 600
            },
            {
                "event_type": "Antivirus Detection",
                "severity": "low",
                "source_ip": "192.168.1.45",
                "dest_ip": "N/A",
                "message": f"Low-risk adware detected and quarantined. No system compromise detected. [{demo_marker}]",
                "minutes_ago": 660
            },
            {
                "event_type": "Login Success",
                "severity": "low",
                "source_ip": "192.168.1.30",
                "dest_ip": "192.168.1.10",
                "message": f"Successful administrative login from authorized workstation. Security clearance verified. [{demo_marker}]",
                "minutes_ago": 720
            },
            {
                "event_type": "System Update",
                "severity": "low",
                "source_ip": "192.168.1.100",
                "dest_ip": "Microsoft Update Servers",
                "message": f"Security patches successfully installed. System restart scheduled for maintenance window. [{demo_marker}]",
                "minutes_ago": 780
            }
        ]
        
        created_count = 0
        
        # Create the demo logs
        for log_data in demo_logs_data:
            timestamp = datetime.now(timezone.utc) - timedelta(minutes=log_data['minutes_ago'])
            
            db_log = SecurityLog(
                timestamp=timestamp,
                source_ip=log_data['source_ip'],
                dest_ip=log_data['dest_ip'],
                event_type=log_data['event_type'],
                severity=log_data['severity'],
                message=log_data['message']
            )
            
            db.add(db_log)
            created_count += 1
        
        db.commit()
        
        # Print summary
        total_logs = db.query(SecurityLog).count()
        critical_count = db.query(SecurityLog).filter(SecurityLog.severity == 'critical').count()
        high_count = db.query(SecurityLog).filter(SecurityLog.severity == 'high').count()
        medium_count = db.query(SecurityLog).filter(SecurityLog.severity == 'medium').count()
        low_count = db.query(SecurityLog).filter(SecurityLog.severity == 'low').count()
        
        print(f"✅ Successfully created {created_count} persistent demo logs")
        print(f"\n📊 Database Summary:")
        print(f"   Total logs: {total_logs}")
        print(f"   Critical: {critical_count}")
        print(f"   High: {high_count}")  
        print(f"   Medium: {medium_count}")
        print(f"   Low: {low_count}")
        print(f"\n🎯 These logs will persist and be shown every time you open the app.")
        print(f"🔄 The 'Generate Log' button will add new logs to this existing set.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating persistent demo logs: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🛡️  Cyber Defense Assistant - Persistent Demo Data Setup")
    print("=" * 65)
    setup_persistent_demo_data()
