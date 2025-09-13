#!/usr/bin/env python3
"""
Initialize the database with comprehensive persistent demo logs
that will always be available when the application starts.
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import random

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import SecurityLog, Base

def init_persistent_demo_data():
    """Initialize comprehensive demo data that persists across app restarts"""
    
    # Database setup
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cyber_defense.db")
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if persistent demo data already exists
        demo_marker = "PERSISTENT_DEMO"
        existing_count = db.query(SecurityLog).filter(SecurityLog.message.like(f"%{demo_marker}%")).count()
        
        if existing_count > 0:
            print(f"✅ Found {existing_count} existing persistent demo logs")
            return existing_count
        
        print("🔄 Creating comprehensive persistent demo logs...")
        
        # Comprehensive demo log dataset
        demo_logs = [
            # Critical Threats (Most Recent)
            {
                "event_type": "Zero-Day Exploit",
                "severity": "critical",
                "source_ip": "203.0.113.45",
                "dest_ip": "192.168.1.100",
                "message": f"Advanced zero-day exploit targeting military infrastructure. Immediate containment required. Command escalation initiated. [{demo_marker}]",
                "minutes_ago": 5
            },
            {
                "event_type": "Nation-State Actor",
                "severity": "critical", 
                "source_ip": "45.76.212.198",
                "dest_ip": "192.168.1.50",
                "message": f"APT29 signature detected. Sophisticated persistence mechanism deployed. Military secrets at risk. [{demo_marker}]",
                "minutes_ago": 25
            },
            {
                "event_type": "Ransomware Attack",
                "severity": "critical",
                "source_ip": "192.168.1.65",
                "dest_ip": "192.168.1.0/24",
                "message": f"Military-grade ransomware detected. Encryption of classified files prevented. Threat actor communication intercepted. [{demo_marker}]",
                "minutes_ago": 45
            },
            {
                "event_type": "Data Exfiltration",
                "severity": "critical",
                "source_ip": "192.168.1.75", 
                "dest_ip": "104.244.42.129",
                "message": f"Large data transfer (5.2GB) to hostile nation IP. Classified military documents detected in stream. [{demo_marker}]",
                "minutes_ago": 70
            },
            
            # High Severity Threats
            {
                "event_type": "Advanced Malware",
                "severity": "high",
                "source_ip": "198.51.100.23",
                "dest_ip": "192.168.1.205", 
                "message": f"Sophisticated malware with anti-analysis capabilities. Rootkit installation blocked. C2 server identified. [{demo_marker}]",
                "minutes_ago": 90
            },
            {
                "event_type": "SQL Injection Attack",
                "severity": "high",
                "source_ip": "93.184.216.34",
                "dest_ip": "192.168.1.100",
                "message": f"Advanced SQL injection targeting personnel database. 127 injection attempts. Military ID numbers compromised. [{demo_marker}]",
                "minutes_ago": 120
            },
            {
                "event_type": "Credential Compromise",
                "severity": "high",
                "source_ip": "185.220.101.42",
                "dest_ip": "192.168.1.150",
                "message": f"High-clearance military credentials detected on dark web. Immediate password reset protocol activated. [{demo_marker}]",
                "minutes_ago": 150
            },
            {
                "event_type": "Insider Threat",
                "severity": "high",
                "source_ip": "192.168.1.85",
                "dest_ip": "192.168.1.220",
                "message": f"Unusual file access pattern detected. Employee accessing classified files during off-hours. Behavioral anomaly confirmed. [{demo_marker}]",
                "minutes_ago": 180
            },
            {
                "event_type": "Network Intrusion",
                "severity": "high",
                "source_ip": "172.16.0.100",
                "dest_ip": "192.168.1.0/24",
                "message": f"Lateral movement detected across network segments. Multiple systems compromised. Attack in progress. [{demo_marker}]",
                "minutes_ago": 210
            },
            
            # Medium Severity Events
            {
                "event_type": "Spear Phishing",
                "severity": "medium",
                "source_ip": "172.16.254.78",
                "dest_ip": "192.168.1.150",
                "message": f"Targeted spear-phishing campaign against military personnel. Social engineering with unit-specific information. [{demo_marker}]",
                "minutes_ago": 240
            },
            {
                "event_type": "Suspicious Traffic",
                "severity": "medium",
                "source_ip": "198.18.0.100", 
                "dest_ip": "192.168.1.0/24",
                "message": f"Encrypted traffic to suspicious geographic region. Possible covert communication channel. [{demo_marker}]",
                "minutes_ago": 300
            },
            {
                "event_type": "Policy Violation",
                "severity": "medium",
                "source_ip": "192.168.1.90",
                "dest_ip": "52.96.128.0",
                "message": f"Unauthorized cloud storage access detected. Military documents uploaded to civilian service. [{demo_marker}]",
                "minutes_ago": 360
            },
            {
                "event_type": "Firewall Alert",
                "severity": "medium",
                "source_ip": "10.0.0.45",
                "dest_ip": "192.168.1.200",
                "message": f"Multiple blocked connection attempts to restricted military network segments. Reconnaissance suspected. [{demo_marker}]",
                "minutes_ago": 420
            },
            {
                "event_type": "DNS Tunneling",
                "severity": "medium",
                "source_ip": "192.168.1.120",
                "dest_ip": "8.8.8.8",
                "message": f"Suspicious DNS query pattern detected. Possible DNS tunneling for data exfiltration or C2 communication. [{demo_marker}]",
                "minutes_ago": 480
            },
            
            # Low Severity (Routine Operations)
            {
                "event_type": "Authentication Success",
                "severity": "low",
                "source_ip": "192.168.1.30",
                "dest_ip": "192.168.1.10",
                "message": f"Successful multi-factor authentication for classified system access. Security clearance verified. [{demo_marker}]",
                "minutes_ago": 540
            },
            {
                "event_type": "Security Patch",
                "severity": "low",
                "source_ip": "192.168.1.100",
                "dest_ip": "Microsoft Update",
                "message": f"Critical security patches installed successfully. Military systems hardening completed. [{demo_marker}]",
                "minutes_ago": 600
            },
            {
                "event_type": "Antivirus Scan",
                "severity": "low",
                "source_ip": "192.168.1.45",
                "dest_ip": "N/A",
                "message": f"Scheduled antivirus scan completed. 0 threats detected. All military workstations secure. [{demo_marker}]",
                "minutes_ago": 660
            },
            {
                "event_type": "Backup Completion",
                "severity": "low",
                "source_ip": "192.168.1.200",
                "dest_ip": "192.168.1.250",
                "message": f"Automated backup of classified databases completed successfully. Data integrity verified. [{demo_marker}]",
                "minutes_ago": 720
            },
            {
                "event_type": "System Monitoring",
                "severity": "low",
                "source_ip": "192.168.1.10",
                "dest_ip": "N/A",
                "message": f"Routine system health check completed. All military network components operational. [{demo_marker}]",
                "minutes_ago": 780
            }
        ]
        
        created_count = 0
        
        # Create all demo logs
        for log_data in demo_logs:
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
        
        # Print detailed summary
        total_logs = db.query(SecurityLog).count()
        critical_count = db.query(SecurityLog).filter(SecurityLog.severity == 'critical').count()
        high_count = db.query(SecurityLog).filter(SecurityLog.severity == 'high').count()
        medium_count = db.query(SecurityLog).filter(SecurityLog.severity == 'medium').count()
        low_count = db.query(SecurityLog).filter(SecurityLog.severity == 'low').count()
        
        print(f"✅ Successfully created {created_count} persistent demo logs")
        print(f"\n📊 Database Summary:")
        print(f"   Total logs: {total_logs}")
        print(f"   🔴 Critical: {critical_count}")
        print(f"   🟠 High: {high_count}")
        print(f"   🟡 Medium: {medium_count}")
        print(f"   🟢 Low: {low_count}")
        print(f"\n🎯 These logs will persist across application restarts")
        print(f"🔄 The 'Generate Log' button will add new logs to this set")
        
        return created_count
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating persistent demo logs: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🛡️  Cyber Defense Assistant - Database Initialization")
    print("=" * 60)
    count = init_persistent_demo_data()
    print(f"\n🚀 Database initialization complete! Created {count} demo logs.")
