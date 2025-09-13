#!/usr/bin/env python3
"""
Quick demo data generator for the Cyber Defense Assistant
"""

import requests
import json
from datetime import datetime, timedelta
import random
import time

# Configuration
API_BASE_URL = "http://localhost:8000"
LOGS_ENDPOINT = f"{API_BASE_URL}/logs"

# Sample data for generating realistic fake logs
DEMO_SCENARIOS = [
    {
        "event_type": "brute_force_ssh",
        "severity": "high",
        "source_ips": ["192.168.1.100", "10.0.0.45", "172.16.0.23", "203.0.113.42"],
        "dest_ips": ["10.0.1.50", "192.168.1.10"],
        "messages": [
            "Multiple failed SSH login attempts detected from external IP",
            "SSH brute force attack in progress - 50+ failed attempts",
            "Excessive authentication failures from suspicious source IP",
            "SSH login attempts with common usernames detected"
        ]
    },
    {
        "event_type": "malware_detection",
        "severity": "critical",
        "source_ips": ["192.168.1.75", "10.0.0.33", "172.16.0.88"],
        "dest_ips": ["8.8.8.8", "1.1.1.1", "suspicious-domain.com", "malicious-c2.net"],
        "messages": [
            "Trojan.Generic detected on workstation - quarantined",
            "C2 communication attempt blocked by firewall",
            "Suspicious executable behavior detected by endpoint protection",
            "Malware signature match in network traffic analysis",
            "Ransomware encryption activity detected and stopped"
        ]
    },
    {
        "event_type": "port_scan",
        "severity": "medium",
        "source_ips": ["203.0.113.15", "198.51.100.200", "192.0.2.88", "185.220.101.42"],
        "dest_ips": ["10.0.1.100", "192.168.1.50", "172.16.0.100"],
        "messages": [
            "Sequential port scanning activity detected",
            "Network reconnaissance attempt from external source",
            "Stealth port scan identified targeting critical servers",
            "Multiple service discovery attempts logged"
        ]
    },
    {
        "event_type": "failed_login",
        "severity": "medium",
        "source_ips": ["192.168.1.200", "10.0.0.75", "172.16.0.150"],
        "dest_ips": ["10.0.1.10", "192.168.1.5", "ad-server.local"],
        "messages": [
            "Multiple authentication failures for admin accounts",
            "Account lockout threshold exceeded for user account",
            "Invalid credentials provided for privileged access",
            "Suspicious login pattern detected during off-hours"
        ]
    },
    {
        "event_type": "intrusion_attempt",
        "severity": "high",
        "source_ips": ["192.0.2.150", "203.0.113.75", "198.51.100.42"],
        "dest_ips": ["10.0.1.20", "192.168.1.30", "web-server.local"],
        "messages": [
            "SQL injection attempt blocked by web application firewall",
            "Buffer overflow exploit detected and prevented",
            "Unauthorized privilege escalation attempt identified",
            "Command injection payload detected in HTTP request",
            "Directory traversal attack attempt logged"
        ]
    },
    {
        "event_type": "firewall_block",
        "severity": "low",
        "source_ips": ["203.0.113.100", "198.51.100.250", "185.220.102.15"],
        "dest_ips": ["10.0.1.0", "192.168.1.0", "172.16.0.0"],
        "messages": [
            "Outbound connection blocked by security policy",
            "Suspicious traffic filtered by perimeter firewall",
            "Geo-blocking rule triggered for high-risk country",
            "Protocol violation detected and connection dropped"
        ]
    }
]

def generate_demo_log():
    """Generate a realistic demo security log entry."""
    scenario = random.choice(DEMO_SCENARIOS)
    
    # Generate timestamp within last 6 hours with some clustering
    now = datetime.utcnow()
    
    # Create some time clusters for more realistic attack patterns
    if random.random() < 0.3:  # 30% chance of recent activity (last 30 minutes)
        random_minutes = random.randint(0, 30)
    elif random.random() < 0.5:  # 20% chance of activity 1-2 hours ago
        random_minutes = random.randint(60, 120)
    else:  # 50% chance of older activity (2-6 hours ago)
        random_minutes = random.randint(120, 360)
    
    timestamp = now - timedelta(minutes=random_minutes)
    
    log_entry = {
        "timestamp": timestamp.isoformat() + "Z",
        "source_ip": random.choice(scenario["source_ips"]),
        "dest_ip": random.choice(scenario["dest_ips"]),
        "event_type": scenario["event_type"],
        "severity": scenario["severity"],
        "message": random.choice(scenario["messages"])
    }
    
    return log_entry

def send_log(log_entry):
    """Send a log entry to the API."""
    try:
        response = requests.post(LOGS_ENDPOINT, json=log_entry)
        if response.status_code == 200:
            return True
        else:
            print(f"❌ Failed to send log: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def populate_demo_data(num_logs=75):
    """Populate the database with demo security logs."""
    print(f"🚀 Generating {num_logs} demo security logs...")
    print("=" * 50)
    
    successful = 0
    failed = 0
    
    for i in range(num_logs):
        log_entry = generate_demo_log()
        if send_log(log_entry):
            successful += 1
            print(f"✅ {log_entry['event_type']} - {log_entry['severity'].upper()}")
        else:
            failed += 1
        
        # Small delay to avoid overwhelming the API
        time.sleep(0.05)
        
        # Show progress
        if (i + 1) % 15 == 0:
            print(f"📊 Progress: {i + 1}/{num_logs} logs processed")
    
    print(f"\n🎉 Demo data generation completed!")
    print(f"✅ Successfully sent: {successful} logs")
    print(f"❌ Failed to send: {failed} logs")
    print(f"🎯 Total processed: {successful + failed} logs")
    print(f"\n🌐 Open http://localhost:3000 to view the dashboard!")

if __name__ == "__main__":
    print("🛡️ Cyber Defense Assistant - Demo Data Generator")
    print("=" * 55)
    
    try:
        # Test API connectivity
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend API is running")
            populate_demo_data()
        else:
            print("❌ Backend API is not responding properly")
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to backend API at http://localhost:8000")
        print("Please make sure the backend is running with: python3 main.py")
