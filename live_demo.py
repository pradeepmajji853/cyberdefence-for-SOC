#!/usr/bin/env python3
"""
Live Demo Script for Cyber Defense Assistant
Generates realistic security incidents during presentations
"""

import requests
import json
from datetime import datetime
import random
import time
import threading

# Configuration
API_BASE_URL = "http://localhost:8000"
LOGS_ENDPOINT = f"{API_BASE_URL}/logs"

class LiveDemoGenerator:
    def __init__(self):
        self.running = False
        self.thread = None
        
    def start_attack_simulation(self, attack_type="mixed"):
        """Start simulating a specific type of attack"""
        self.running = True
        
        if attack_type == "brute_force":
            self.thread = threading.Thread(target=self._simulate_brute_force)
        elif attack_type == "malware_outbreak":
            self.thread = threading.Thread(target=self._simulate_malware_outbreak)
        elif attack_type == "port_scan":
            self.thread = threading.Thread(target=self._simulate_port_scan)
        elif attack_type == "mixed":
            self.thread = threading.Thread(target=self._simulate_mixed_attacks)
        
        self.thread.start()
        
    def stop_simulation(self):
        """Stop the attack simulation"""
        self.running = False
        if self.thread:
            self.thread.join()
            
    def _simulate_brute_force(self):
        """Simulate an ongoing brute force attack"""
        print("🚨 SIMULATING: SSH Brute Force Attack Campaign")
        
        attacker_ips = ["203.0.113.42", "198.51.100.15", "192.0.2.88"]
        target_servers = ["10.0.1.50", "192.168.1.10", "172.16.0.25"]
        
        attack_count = 0
        while self.running and attack_count < 20:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "source_ip": random.choice(attacker_ips),
                "dest_ip": random.choice(target_servers),
                "event_type": "brute_force_ssh",
                "severity": "high",
                "message": f"SSH brute force attempt #{attack_count + 1} - Failed login with username: {random.choice(['admin', 'root', 'administrator', 'user'])}"
            }
            
            self._send_log(log_entry)
            attack_count += 1
            time.sleep(random.uniform(2, 5))
            
    def _simulate_malware_outbreak(self):
        """Simulate malware detection across multiple systems"""
        print("🦠 SIMULATING: Malware Outbreak Detection")
        
        infected_hosts = ["192.168.1.75", "192.168.1.82", "192.168.1.91", "192.168.1.105"]
        c2_servers = ["malicious-c2.net", "evil-domain.com", "bad-actor.org"]
        
        for i in range(15):
            if not self.running:
                break
                
            log_entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "source_ip": random.choice(infected_hosts),
                "dest_ip": random.choice(c2_servers),
                "event_type": "malware_detection",
                "severity": "critical",
                "message": f"Malware communication detected - Host attempting C2 contact #{i+1}"
            }
            
            self._send_log(log_entry)
            time.sleep(random.uniform(3, 8))
            
    def _simulate_port_scan(self):
        """Simulate network reconnaissance"""
        print("🔍 SIMULATING: Network Reconnaissance Campaign")
        
        scanner_ip = "185.220.101.42"
        target_range = ["10.0.1.100", "10.0.1.101", "10.0.1.102", "10.0.1.103"]
        
        for target in target_range:
            for scan_type in ["TCP SYN scan", "UDP scan", "Service enumeration"]:
                if not self.running:
                    break
                    
                log_entry = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "source_ip": scanner_ip,
                    "dest_ip": target,
                    "event_type": "port_scan",
                    "severity": "medium",
                    "message": f"{scan_type} detected against {target}"
                }
                
                self._send_log(log_entry)
                time.sleep(1)
                
    def _simulate_mixed_attacks(self):
        """Simulate various mixed security events"""
        print("⚡ SIMULATING: Mixed Security Events")
        
        events = [
            {
                "event_type": "failed_login",
                "severity": "medium",
                "source_ip": "192.168.1.200",
                "dest_ip": "ad-server.local",
                "message": "Multiple failed login attempts for privileged account"
            },
            {
                "event_type": "intrusion_attempt",
                "severity": "high",
                "source_ip": "203.0.113.75",
                "dest_ip": "web-server.local",
                "message": "SQL injection attempt blocked by WAF"
            },
            {
                "event_type": "firewall_block",
                "severity": "low",
                "source_ip": "198.51.100.250",
                "dest_ip": "10.0.1.0",
                "message": "Suspicious outbound connection blocked"
            }
        ]
        
        event_count = 0
        while self.running and event_count < 25:
            event = random.choice(events)
            log_entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                **event
            }
            
            self._send_log(log_entry)
            event_count += 1
            time.sleep(random.uniform(4, 10))
            
    def _send_log(self, log_entry):
        """Send a log entry to the API"""
        try:
            response = requests.post(LOGS_ENDPOINT, json=log_entry)
            if response.status_code == 200:
                print(f"📝 {log_entry['event_type']} - {log_entry['severity'].upper()}")
            else:
                print(f"❌ Failed to send log: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")

def main():
    """Main demo interface"""
    generator = LiveDemoGenerator()
    
    print("🛡️ CYBER DEFENSE ASSISTANT - LIVE DEMO CONTROLLER")
    print("=" * 60)
    print("This script generates live security events for demonstration")
    print("Make sure the dashboard is open at http://localhost:3000")
    print("=" * 60)
    
    try:
        while True:
            print("\n🎭 DEMO SCENARIOS:")
            print("1. 🚨 SSH Brute Force Attack")
            print("2. 🦠 Malware Outbreak")
            print("3. 🔍 Network Port Scanning")
            print("4. ⚡ Mixed Security Events")
            print("5. ⏹️  Stop Current Simulation")
            print("6. 🚪 Exit Demo Controller")
            
            choice = input("\nSelect scenario (1-6): ").strip()
            
            if choice == "1":
                if not generator.running:
                    generator.start_attack_simulation("brute_force")
                    print("✅ Brute force simulation started")
                else:
                    print("⚠️ Simulation already running")
                    
            elif choice == "2":
                if not generator.running:
                    generator.start_attack_simulation("malware_outbreak")
                    print("✅ Malware outbreak simulation started")
                else:
                    print("⚠️ Simulation already running")
                    
            elif choice == "3":
                if not generator.running:
                    generator.start_attack_simulation("port_scan")
                    print("✅ Port scan simulation started")
                else:
                    print("⚠️ Simulation already running")
                    
            elif choice == "4":
                if not generator.running:
                    generator.start_attack_simulation("mixed")
                    print("✅ Mixed events simulation started")
                else:
                    print("⚠️ Simulation already running")
                    
            elif choice == "5":
                if generator.running:
                    generator.stop_simulation()
                    print("⏹️ Simulation stopped")
                else:
                    print("⚠️ No simulation running")
                    
            elif choice == "6":
                if generator.running:
                    generator.stop_simulation()
                print("👋 Exiting demo controller")
                break
                
            else:
                print("❌ Invalid choice")
                
    except KeyboardInterrupt:
        if generator.running:
            generator.stop_simulation()
        print("\n👋 Demo controller stopped")

if __name__ == "__main__":
    main()
