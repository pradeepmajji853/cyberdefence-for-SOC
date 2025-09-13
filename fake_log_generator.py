import requests
import json
from datetime import datetime, timedelta
import random
import time

# Configuration
API_BASE_URL = "http://localhost:8000"
LOGS_ENDPOINT = f"{API_BASE_URL}/logs"

# Sample data for generating realistic fake logs
ATTACK_SCENARIOS = [
    {
        "event_type": "brute_force_ssh",
        "severity": "high",
        "source_ips": ["192.168.1.100", "10.0.0.45", "172.16.0.23"],
        "dest_ips": ["10.0.1.50", "192.168.1.10"],
        "messages": [
            "Multiple failed SSH login attempts detected",
            "SSH brute force attack in progress",
            "Excessive authentication failures from source IP"
        ]
    },
    {
        "event_type": "port_scan",
        "severity": "medium",
        "source_ips": ["203.0.113.42", "198.51.100.15", "192.0.2.88"],
        "dest_ips": ["10.0.1.100", "192.168.1.50", "172.16.0.100"],
        "messages": [
            "Port scanning activity detected",
            "Sequential port probing from external IP",
            "Network reconnaissance attempt identified"
        ]
    },
    {
        "event_type": "malware_detection",
        "severity": "critical",
        "source_ips": ["192.168.1.75", "10.0.0.33"],
        "dest_ips": ["8.8.8.8", "1.1.1.1", "malicious-domain.com"],
        "messages": [
            "Malware signature detected in network traffic",
            "C2 communication attempt blocked",
            "Suspicious executable behavior detected",
            "Trojan communication to known C2 server"
        ]
    },
    {
        "event_type": "ddos_attack",
        "severity": "critical",
        "source_ips": ["203.0.113.0", "198.51.100.0", "192.0.2.0"],
        "dest_ips": ["10.0.1.1", "192.168.1.1"],
        "messages": [
            "High volume traffic detected",
            "DDoS attack in progress",
            "Server resources under heavy load",
            "Network bandwidth saturation detected"
        ]
    },
    {
        "event_type": "failed_login",
        "severity": "medium",
        "source_ips": ["192.168.1.200", "10.0.0.75"],
        "dest_ips": ["10.0.1.10", "192.168.1.5"],
        "messages": [
            "Authentication failure recorded",
            "Invalid credentials provided",
            "Account lockout threshold exceeded"
        ]
    },
    {
        "event_type": "firewall_block",
        "severity": "low",
        "source_ips": ["203.0.113.100", "198.51.100.200"],
        "dest_ips": ["10.0.1.0", "192.168.1.0"],
        "messages": [
            "Firewall rule triggered",
            "Blocked connection attempt",
            "Traffic filtered by security policy"
        ]
    },
    {
        "event_type": "intrusion_attempt",
        "severity": "high",
        "source_ips": ["192.0.2.150", "203.0.113.75"],
        "dest_ips": ["10.0.1.20", "192.168.1.30"],
        "messages": [
            "IDS signature match detected",
            "Potential system compromise attempt",
            "Unauthorized access attempt blocked",
            "Exploit payload detected in traffic"
        ]
    }
]

def generate_fake_log():
    """Generate a realistic fake security log entry."""
    scenario = random.choice(ATTACK_SCENARIOS)
    
    # Generate timestamp within last 4 hours
    now = datetime.utcnow()
    random_minutes = random.randint(0, 240)  # 0 to 4 hours ago
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
            print(f"✅ Sent: {log_entry['event_type']} - {log_entry['severity']}")
            return True
        else:
            print(f"❌ Failed to send log: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def populate_database(num_logs=50):
    """Populate the database with fake security logs."""
    print(f"🚀 Generating {num_logs} fake security logs...")
    
    successful = 0
    failed = 0
    
    for i in range(num_logs):
        log_entry = generate_fake_log()
        if send_log(log_entry):
            successful += 1
        else:
            failed += 1
        
        # Small delay to avoid overwhelming the API
        time.sleep(0.1)
        
        # Show progress every 10 logs
        if (i + 1) % 10 == 0:
            print(f"Progress: {i + 1}/{num_logs} logs processed")
    
    print(f"\n📊 Results:")
    print(f"✅ Successfully sent: {successful} logs")
    print(f"❌ Failed to send: {failed} logs")
    print(f"🎯 Total processed: {successful + failed} logs")

def simulate_live_feed(duration_minutes=5, logs_per_minute=3):
    """Simulate live security events for demo purposes."""
    print(f"🔴 Starting live simulation for {duration_minutes} minutes...")
    print(f"📈 Generating ~{logs_per_minute} logs per minute")
    
    end_time = datetime.utcnow() + timedelta(minutes=duration_minutes)
    log_count = 0
    
    while datetime.utcnow() < end_time:
        # Generate logs at specified rate
        for _ in range(logs_per_minute):
            log_entry = generate_fake_log()
            # Override timestamp to be current for live simulation
            log_entry["timestamp"] = datetime.utcnow().isoformat() + "Z"
            
            if send_log(log_entry):
                log_count += 1
            
            # Wait between logs within the minute
            time.sleep(60 / logs_per_minute)
    
    print(f"\n🏁 Live simulation completed!")
    print(f"📊 Total logs generated: {log_count}")

if __name__ == "__main__":
    print("🛡️ Cyber Defense Assistant - Log Generator")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Populate database with historical logs")
        print("2. Start live log simulation")
        print("3. Generate single test log")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            try:
                num = int(input("Enter number of logs to generate (default: 50): ") or "50")
                populate_database(num)
            except ValueError:
                print("❌ Invalid number entered")
        
        elif choice == "2":
            try:
                duration = int(input("Enter simulation duration in minutes (default: 5): ") or "5")
                rate = int(input("Enter logs per minute (default: 3): ") or "3")
                simulate_live_feed(duration, rate)
            except ValueError:
                print("❌ Invalid input entered")
        
        elif choice == "3":
            log = generate_fake_log()
            print(f"\n📋 Generated log:")
            print(json.dumps(log, indent=2))
            if input("\nSend this log? (y/N): ").lower() == 'y':
                send_log(log)
        
        elif choice == "4":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-4.")
