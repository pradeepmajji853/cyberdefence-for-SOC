#!/usr/bin/env python3
"""
🛡️ Advanced Cyber Defense CLI - Enhanced Version
==================================================

Advanced CLI with additional features:
- Batch operations
- Configuration management  
- Export capabilities
- System health monitoring
- Performance metrics
"""

import os
import json
import time
from datetime import datetime
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.progress import track
import argparse

console = Console()

class AdvancedCyberDefenseCLI:
    def __init__(self):
        self.api_base = "http://localhost:8001"
        self.config_file = "cli_config.json"
        self.load_config()
    
    def load_config(self):
        """Load CLI configuration"""
        default_config = {
            "api_url": "http://localhost:8001",
            "default_log_limit": 10,
            "monitor_interval": 5,
            "auto_refresh": True
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Save CLI configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def batch_simulate_attacks(self, attack_list, delay=2):
        """Simulate multiple attacks in sequence"""
        results = []
        
        console.print(f"🚀 [bold cyan]Running batch attack simulation...[/bold cyan]")
        
        for attack in track(attack_list, description="Simulating attacks..."):
            try:
                response = requests.post(
                    f"{self.api_base}/simulate-attack",
                    params={"attack_type": attack}
                )
                if response.status_code == 200:
                    result = response.json()
                    results.append({
                        "attack": attack,
                        "status": "success",
                        "logs_created": result.get("logs_created", 0)
                    })
                    console.print(f"  ✅ {attack}: {result.get('logs_created', 0)} events")
                else:
                    results.append({
                        "attack": attack,
                        "status": "failed",
                        "error": f"HTTP {response.status_code}"
                    })
                    console.print(f"  ❌ {attack}: Failed")
            except Exception as e:
                results.append({
                    "attack": attack,
                    "status": "error",
                    "error": str(e)
                })
                console.print(f"  ❌ {attack}: Error")
            
            if delay > 0:
                time.sleep(delay)
        
        return results
    
    def export_logs_detailed(self, format="json", severity=None, hours_back=24):
        """Export logs with detailed formatting"""
        try:
            params = {"limit": 1000, "hours_back": hours_back}
            if severity:
                params["severity"] = severity
            
            response = requests.get(f"{self.api_base}/logs", params=params)
            if response.status_code == 200:
                logs = response.json()
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                if format.lower() == "json":
                    filename = f"cyber_logs_detailed_{timestamp}.json"
                    with open(filename, 'w') as f:
                        json.dump({
                            "export_info": {
                                "timestamp": datetime.now().isoformat(),
                                "total_logs": len(logs),
                                "severity_filter": severity,
                                "hours_back": hours_back
                            },
                            "logs": logs
                        }, f, indent=2, default=str)
                
                elif format.lower() == "csv":
                    import csv
                    filename = f"cyber_logs_detailed_{timestamp}.csv"
                    with open(filename, 'w', newline='') as f:
                        if logs:
                            writer = csv.DictWriter(f, fieldnames=logs[0].keys())
                            writer.writeheader()
                            writer.writerows(logs)
                
                console.print(f"📊 Exported {len(logs)} logs to: [green]{filename}[/green]")
                return filename
            else:
                console.print(f"❌ Export failed: HTTP {response.status_code}")
                return None
        except Exception as e:
            console.print(f"❌ Export error: {e}")
            return None
    
    def system_health_report(self):
        """Generate comprehensive system health report"""
        console.print("🏥 [bold cyan]Generating System Health Report...[/bold cyan]")
        
        health_data = {}
        
        # Check backend
        try:
            response = requests.get(f"{self.api_base}/health", timeout=5)
            health_data["backend"] = {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds()
            }
        except Exception as e:
            health_data["backend"] = {"status": "down", "error": str(e)}
        
        # Check logs count
        try:
            response = requests.get(f"{self.api_base}/stats")
            if response.status_code == 200:
                stats = response.json()
                health_data["database"] = {
                    "total_logs": stats.get("total_logs", 0),
                    "critical_events": stats.get("critical_count", 0)
                }
        except:
            health_data["database"] = {"status": "unavailable"}
        
        # Performance test
        console.print("  🔍 Running performance tests...")
        start_time = time.time()
        try:
            for _ in range(3):
                requests.get(f"{self.api_base}/logs", params={"limit": 10})
            avg_response = (time.time() - start_time) / 3
            health_data["performance"] = {
                "avg_response_time": round(avg_response, 3),
                "status": "good" if avg_response < 1.0 else "slow"
            }
        except:
            health_data["performance"] = {"status": "failed"}
        
        # Generate report
        table = Table(title="🏥 System Health Report", box=box.ROUNDED)
        table.add_column("Component", style="cyan")
        table.add_column("Status", justify="center")
        table.add_column("Details")
        
        # Backend status
        backend = health_data.get("backend", {})
        status = "✅ Healthy" if backend.get("status") == "healthy" else "❌ Unhealthy"
        details = f"Response: {backend.get('response_time', 'N/A')}s" if "response_time" in backend else backend.get('error', 'N/A')
        table.add_row("Backend API", status, details)
        
        # Database status
        db = health_data.get("database", {})
        if "total_logs" in db:
            table.add_row("Database", "✅ Connected", f"{db['total_logs']} logs, {db['critical_events']} critical")
        else:
            table.add_row("Database", "❌ Unavailable", "Cannot retrieve stats")
        
        # Performance
        perf = health_data.get("performance", {})
        perf_status = "✅ Good" if perf.get("status") == "good" else "⚠️ Slow"
        perf_details = f"Avg: {perf.get('avg_response_time', 'N/A')}s"
        table.add_row("Performance", perf_status, perf_details)
        
        console.print(table)
        
        # Save report
        report_file = f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "health_data": health_data
            }, f, indent=2)
        
        console.print(f"📋 Health report saved to: [green]{report_file}[/green]")
        return health_data

def main():
    parser = argparse.ArgumentParser(description="🛡️ Advanced Cyber Defense CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Batch simulate
    batch_parser = subparsers.add_parser('batch-simulate', help='Simulate multiple attacks')
    batch_parser.add_argument('attacks', nargs='+', 
                             choices=['ddos', 'phishing', 'insider_threat', 'ransomware'],
                             help='Attack types to simulate')
    batch_parser.add_argument('--delay', type=int, default=2, help='Delay between attacks')
    
    # Enhanced export
    export_parser = subparsers.add_parser('export-logs', help='Export logs with advanced options')
    export_parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Export format')
    export_parser.add_argument('--severity', choices=['critical', 'high', 'medium', 'low'], help='Filter by severity')
    export_parser.add_argument('--hours', type=int, default=24, help='Hours back to export')
    
    # Health report
    health_parser = subparsers.add_parser('health-report', help='Generate system health report')
    
    # Quick setup
    setup_parser = subparsers.add_parser('quick-setup', help='Quick system setup and test')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = AdvancedCyberDefenseCLI()
    
    if args.command == 'batch-simulate':
        cli.batch_simulate_attacks(args.attacks, args.delay)
    
    elif args.command == 'export-logs':
        cli.export_logs_detailed(args.format, args.severity, args.hours)
    
    elif args.command == 'health-report':
        cli.system_health_report()
    
    elif args.command == 'quick-setup':
        console.print("🚀 [bold cyan]Quick System Setup & Test[/bold cyan]")
        
        # 1. Health check
        health = cli.system_health_report()
        
        # 2. Generate test data
        console.print("\n📊 Generating test data...")
        test_attacks = ['ddos', 'phishing']
        cli.batch_simulate_attacks(test_attacks, delay=1)
        
        # 3. Export sample
        console.print("\n📁 Creating sample export...")
        cli.export_logs_detailed("json", severity=None, hours_back=1)
        
        console.print("\n✅ [bold green]Quick setup complete![/bold green]")

if __name__ == "__main__":
    main()
