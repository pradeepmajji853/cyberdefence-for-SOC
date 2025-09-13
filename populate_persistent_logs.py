#!/usr/bin/env python3
"""
Populate the database with a consistent set of demo security logs
that will always be displayed when the application starts.
"""

import os
import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import random

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SecurityLog, Base

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cyber_defense.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def create_persistent_demo_logs():
    """Create a consistent set of demo logs that will always be shown."""
    
    # Predefined log entries that will always appear
    demo_logs = [
        {
            "event_type": "Critical System Breach",
            "severity": "critical",
            "source_ip": "203.0.113.45",
            "dest_ip": "192.168.1.100",
            "message": "Unauthorized root access detected on web server. Multiple authentication bypasses observed.",
            "hours_ago": 0.5
        },
        {
            "event_type": "Malware Detection", 
            "severity": "high",
            "source_ip": "198.51.100.23",
            "dest_ip": "192.168.1.205",
            "message": "Trojan.Win32.Agent detected in email attachment. Quarantine initiated.",
            "hours_ago": 1.2
        },
        {
            "event_type": "DDoS Attack",
            "severity": "high", 
            "source_ip": "185.220.101.42",
            "dest_ip": "192.168.1.1",
            "message": "Volumetric DDoS attack detected. 50,000+ requests per second from botnet.",
            "hours_ago": 2.1
        },
        {
            "event_type": "Phishing Attempt",
            "severity": "medium",
            "source_ip": "172.16.254.78",
            "dest_ip": "192.168.1.150",
            "message": "Suspicious email with credential harvesting link blocked by security filter.",
            "hours_ago": 3.5
        },
        {
            "event_type": "Brute Force SSH",
            "severity": "high",
            "source_ip": "45.76.212.198",
            "dest_ip": "192.168.1.50",
            "message": "Multiple failed SSH login attempts detected. Source IP added to blocklist.",
            "hours_ago": 4.2
        },
        {
            "event_type": "Data Exfiltration",
            "severity": "critical",
            "source_ip": "192.168.1.75",
            "dest_ip": "104.244.42.129", 
            "message": "Large data transfer to external IP detected. Potential data breach in progress.",
            "hours_ago": 5.8
        },
        {
            "event_type": "Firewall Rule Violation",
            "severity": "medium",
            "source_ip": "10.0.0.45",
            "dest_ip": "192.168.1.200",
            "message": "Attempted connection to blocked port 4444. Connection denied by firewall.",
            "hours_ago": 6.5
        },
        {
            "event_type": "Privilege Escalation",
            "severity": "critical",
            "source_ip": "192.168.1.30",
            "dest_ip": "192.168.1.10",
            "message": "User account escalated to admin privileges without authorization. Security policy violation.",
            "hours_ago": 7.1
        },
        {
            "event_type": "SQL Injection Attempt",
            "severity": "high",
            "source_ip": "93.184.216.34",
            "dest_ip": "192.168.1.100",
            "message": "SQL injection attack detected on login form. Malicious queries blocked.",
            "hours_ago": 8.3
        },
        {
            "event_type": "Insider Threat",
            "severity": "high",
            "source_ip": "192.168.1.85",
            "dest_ip": "192.168.1.220",
            "message": "Employee accessing classified files outside working hours. Unusual access pattern detected.",
            "hours_ago": 9.7
        },
        {
            "event_type": "Ransomware Activity",
            "severity": "critical", 
            "source_ip": "192.168.1.65",
            "dest_ip": "192.168.1.0/24",
            "message": "File encryption activity detected. Ransomware signature matches known threat family.",
            "hours_ago": 12.4
        },
        {
            "event_type": "Network Scanner",
            "severity": "medium",
            "source_ip": "198.18.0.100",
            "dest_ip": "192.168.1.0/24", 
            "message": "Network reconnaissance scan detected. Multiple ports probed across subnet.",
            "hours_ago": 15.2
        },
        {
            "event_type": "Failed VPN Login",
            "severity": "low",
            "source_ip": "203.0.113.99",
            "dest_ip": "192.168.1.1",
            "message": "VPN authentication failed for user. Credentials may be compromised.",
            "hours_ago": 18.5
        },
        {
            "event_type": "Unauthorized Software",
            "severity": "medium",
            "source_ip": "192.168.1.90",
            "dest_ip": "52.96.128.0",
            "message": "Installation of unauthorized software detected on workstation. Policy violation.",
            "hours_ago": 20.1
        },
        {
            "event_type": "DNS Tunneling",
            "severity": "high",
            "source_ip": "192.168.1.120",
            "dest_ip": "8.8.8.8",
            "message": "Suspicious DNS queries detected. Potential DNS tunneling for command and control.",
            "hours_ago": 22.8
        }
    ]
    
    db = SessionLocal()
    
    try:
        # Clear existing logs older than 1 day to make room for consistent demo data
        one_day_ago = datetime.utcnow() - timedelta(days=1)
        old_logs_count = db.query(SecurityLog).filter(SecurityLog.timestamp < one_day_ago).count()
        if old_logs_count > 0:
            db.query(SecurityLog).filter(SecurityLog.timestamp < one_day_ago).delete()
            print(f"🗑️  Cleaned up {old_logs_count} old logs")
        
        # Check if demo logs already exist (to avoid duplicates)
        existing_demo_logs = db.query(SecurityLog).filter(
            SecurityLog.message.like("%Unauthorized root access detected%")
        ).count()
        
        if existing_demo_logs > 0:
            print(f"ℹ️  Demo logs already exist ({existing_demo_logs} found). Skipping creation.")
            db.close()
            return
        
        created_count = 0
        
        for log_data in demo_logs:
            # Calculate timestamp based on hours ago
            timestamp = datetime.utcnow() - timedelta(hours=log_data['hours_ago'])
            
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
        
        # Add some additional random logs for variety
        additional_events = [
            "Login Success", "Firewall Block", "Antivirus Scan", "System Update", 
            "Configuration Change", "Password Reset", "File Access", "Network Connection"
        ]
        
        severities = ["low", "medium", "high"]
        
        for i in range(10):
            hours_ago = random.uniform(0.1, 23.5)
            timestamp = datetime.utcnow() - timedelta(hours=hours_ago)
            
            db_log = SecurityLog(
                timestamp=timestamp,
                source_ip=f"192.168.{random.randint(1, 10)}.{random.randint(1, 254)}",
                dest_ip=f"10.0.{random.randint(1, 10)}.{random.randint(1, 254)}",
                event_type=random.choice(additional_events),
                severity=random.choice(severities),
                message=f"Standard security event - {random.choice(['routine monitoring', 'automated scan', 'scheduled maintenance', 'normal operation'])}"
            )
            
            db.add(db_log)
            created_count += 1
        
        db.commit()
        print(f"✅ Successfully created {created_count} persistent demo logs")
        
        # Display summary
        total_logs = db.query(SecurityLog).count()
        critical_logs = db.query(SecurityLog).filter(SecurityLog.severity == 'critical').count()
        high_logs = db.query(SecurityLog).filter(SecurityLog.severity == 'high').count()
        
        print(f"📊 Database Summary:")
        print(f"   Total logs: {total_logs}")
        print(f"   Critical: {critical_logs}")
        print(f"   High: {high_logs}")
        print(f"   Recent 24h: {db.query(SecurityLog).filter(SecurityLog.timestamp >= datetime.utcnow() - timedelta(days=1)).count()}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating demo logs: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🛡️  Cyber Defense Assistant - Persistent Demo Data Setup")
    print("=" * 60)
    create_persistent_demo_logs()
    print("\n🎯 Demo logs are now ready!")
    print("💡 These logs will persist and be shown every time you open the app.")
    print("🔄 The 'Generate Log' button will add new logs to this existing set.")
