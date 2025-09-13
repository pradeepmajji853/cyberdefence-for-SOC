#!/usr/bin/env python3
"""
🛡️ Cyber Defense Assistant - Command Line Interface
====================================================

A comprehensive CLI tool for interacting with the AI-Powered Cyber Defense System.
Provides command-line access to attack simulations, log management, AI analysis, and system monitoring.

Usage:
    python3 cyber_defense_cli.py [command] [options]

Commands:
    status          - Check system status
    simulate        - Run attack simulations
    logs            - Manage security logs
    chat            - Interactive AI chat
    analyze         - Get AI threat analysis
    stats           - View system statistics
    monitor         - Real-time monitoring
    actions         - Execute security actions
    demo            - Run demo scenarios
    help            - Show detailed help
"""

import argparse
import json
import time
import sys
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import sqlite3

try:
    import requests
except ImportError:
    print("❌ Error: requests library not found. Install with: pip install requests")
    sys.exit(1)

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
except ImportError:
    print("❌ Error: rich library not found. Install with: pip install rich")
    sys.exit(1)

# Configuration
API_BASE_URL = "http://localhost:8001"
FRONTEND_URL = "http://localhost:3000"
DB_PATH = "cyber_defense.db"

console = Console()

class CyberDefenseCLI:
    """Main CLI class for the Cyber Defense System"""
    
    def __init__(self):
        self.api_base = API_BASE_URL
        self.session = requests.Session()
        
    def check_system_status(self) -> Dict:
        """Check if backend and frontend are running"""
        status = {
            "backend": False,
            "frontend": False,
            "database": False,
            "total_logs": 0
        }
        
        try:
            # Check backend
            response = self.session.get(f"{self.api_base}/health", timeout=3)
            status["backend"] = response.status_code == 200
        except:
            pass
            
        try:
            # Check frontend
            response = self.session.get(FRONTEND_URL, timeout=3)
            status["frontend"] = response.status_code == 200
        except:
            pass
            
        try:
            # Check database
            if os.path.exists(DB_PATH):
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM security_logs")
                status["total_logs"] = cursor.fetchone()[0]
                status["database"] = True
                conn.close()
        except:
            pass
            
        return status
    
    def simulate_attack(self, attack_type: str) -> Dict:
        """Simulate a cyber attack"""
        try:
            response = self.session.post(
                f"{self.api_base}/simulate-attack",
                params={"attack_type": attack_type}
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_logs(self, limit: int = 10, severity: Optional[str] = None) -> List[Dict]:
        """Get security logs"""
        try:
            params = {"limit": limit}
            if severity:
                params["severity"] = severity
            
            response = self.session.get(f"{self.api_base}/logs", params=params)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except:
            return []
    
    def get_analysis(self, hours_back: int = 24) -> Dict:
        """Get AI threat analysis"""
        try:
            response = self.session.get(
                f"{self.api_base}/analysis",
                params={"hours_back": hours_back}
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def chat_with_ai(self, question: str) -> Dict:
        """Chat with AI assistant"""
        try:
            response = self.session.post(
                f"{self.api_base}/chat",
                json={"question": question}
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_stats(self) -> Dict:
        """Get system statistics"""
        try:
            response = self.session.get(f"{self.api_base}/stats")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def execute_action(self, action: str, target: str) -> Dict:
        """Execute security action"""
        try:
            response = self.session.post(
                f"{self.api_base}/execute-action",
                params={"action": action, "target": target}
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

def cmd_status(cli: CyberDefenseCLI, args):
    """Display system status"""
    console.print("\n🔍 [bold cyan]Checking Cyber Defense System Status...[/bold cyan]")
    
    with console.status("Checking services...") as status:
        sys_status = cli.check_system_status()
    
    # Create status table
    table = Table(title="🛡️ System Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Details", style="dim")
    
    # Backend status
    backend_status = "✅ Online" if sys_status["backend"] else "❌ Offline"
    backend_color = "green" if sys_status["backend"] else "red"
    table.add_row("Backend API", f"[{backend_color}]{backend_status}[/{backend_color}]", f"{API_BASE_URL}")
    
    # Frontend status
    frontend_status = "✅ Online" if sys_status["frontend"] else "❌ Offline"
    frontend_color = "green" if sys_status["frontend"] else "red"
    table.add_row("Frontend App", f"[{frontend_color}]{frontend_status}[/{frontend_color}]", f"{FRONTEND_URL}")
    
    # Database status
    db_status = "✅ Connected" if sys_status["database"] else "❌ Not Found"
    db_color = "green" if sys_status["database"] else "red"
    table.add_row("Database", f"[{db_color}]{db_status}[/{db_color}]", f"{sys_status['total_logs']} security logs")
    
    console.print(table)
    
    if not sys_status["backend"]:
        console.print("\n⚠️ [yellow]Backend is offline. Start it with: python3 main.py[/yellow]")
    if not sys_status["frontend"]:
        console.print("⚠️ [yellow]Frontend is offline. Start it with: cd frontend && npm start[/yellow]")

def cmd_simulate(cli: CyberDefenseCLI, args):
    """Run attack simulation"""
    attack_types = {
        "ddos": "DDoS Attack - Distributed Denial of Service",
        "phishing": "Phishing Campaign - Social Engineering",
        "insider_threat": "Insider Threat - Malicious Employee",
        "ransomware": "Ransomware Attack - File Encryption"
    }
    
    if args.type:
        attack_type = args.type.lower()
        if attack_type not in attack_types:
            console.print(f"❌ Invalid attack type. Choose from: {', '.join(attack_types.keys())}")
            return
    else:
        console.print("\n🚨 [bold red]Available Attack Simulations:[/bold red]")
        for key, desc in attack_types.items():
            console.print(f"  {key} - {desc}")
        
        attack_type = Prompt.ask("\nSelect attack type", choices=list(attack_types.keys()))
    
    console.print(f"\n🎯 [bold yellow]Simulating {attack_types[attack_type]}...[/bold yellow]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Running attack simulation...", total=None)
        result = cli.simulate_attack(attack_type)
    
    if "error" in result:
        console.print(f"❌ [red]Simulation failed: {result['error']}[/red]")
        return
    
    # Display results
    panel = Panel(
        f"✅ Attack Type: [bold]{result['attack_type']}[/bold]\n"
        f"📊 Logs Created: [cyan]{result['logs_created']}[/cyan]\n"
        f"💬 Message: {result['message']}",
        title="🚨 Attack Simulation Complete",
        border_style="red"
    )
    console.print(panel)
    
    if args.show_logs:
        console.print("\n📝 [bold]Recent Security Logs:[/bold]")
        logs = cli.get_logs(limit=5)
        for log in logs[:3]:
            timestamp = log.get('timestamp', '')[:19].replace('T', ' ')
            console.print(f"  {timestamp} | [red]{log.get('severity', '')}[/red] | {log.get('message', '')}")

def cmd_logs(cli: CyberDefenseCLI, args):
    """Display security logs"""
    console.print(f"\n📊 [bold cyan]Fetching {args.limit} security logs...[/bold cyan]")
    
    logs = cli.get_logs(limit=args.limit, severity=args.severity)
    
    if not logs:
        console.print("❌ No logs found or backend unavailable")
        return
    
    # Create logs table
    table = Table(title=f"🔐 Security Logs ({len(logs)} entries)")
    table.add_column("Timestamp", style="dim")
    table.add_column("Severity", justify="center")
    table.add_column("Source IP", style="cyan")
    table.add_column("Event Type", style="yellow")
    table.add_column("Message", max_width=60)
    
    for log in logs:
        timestamp = log.get('timestamp', '')[:19].replace('T', ' ')
        severity = log.get('severity', '')
        
        # Color-code severity
        if severity == 'critical':
            severity_colored = f"[bold red]{severity.upper()}[/bold red]"
        elif severity == 'high':
            severity_colored = f"[red]{severity.upper()}[/red]"
        elif severity == 'medium':
            severity_colored = f"[yellow]{severity.upper()}[/yellow]"
        else:
            severity_colored = f"[green]{severity.upper()}[/green]"
        
        table.add_row(
            timestamp,
            severity_colored,
            log.get('source_ip', ''),
            log.get('event_type', ''),
            log.get('message', '')[:80] + ('...' if len(log.get('message', '')) > 80 else '')
        )
    
    console.print(table)
    
    if args.export:
        # Export to JSON
        filename = f"security_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(logs, f, indent=2, default=str)
        console.print(f"📁 Logs exported to: [green]{filename}[/green]")

def cmd_chat(cli: CyberDefenseCLI, args):
    """Interactive chat with AI"""
    if args.message:
        # Single question mode
        console.print(f"\n🤖 [bold cyan]AI Assistant:[/bold cyan] {args.message}")
        
        with console.status("Thinking..."):
            response = cli.chat_with_ai(args.message)
        
        if "error" in response:
            console.print(f"❌ [red]{response['error']}[/red]")
        else:
            console.print(f"\n💬 [bold green]Response:[/bold green] {response.get('answer', 'No response')}")
        return
    
    # Interactive chat mode
    console.print("\n🤖 [bold cyan]Interactive AI Chat - Cyber Defense Assistant[/bold cyan]")
    console.print("Type 'exit' to quit, 'help' for suggestions\n")
    
    suggestions = [
        "What attacks are currently happening?",
        "Show me the most dangerous IPs",
        "What should I do about the recent threats?",
        "Analyze the security logs from the last hour",
        "How severe is the current threat level?"
    ]
    
    while True:
        try:
            question = Prompt.ask("\n[bold blue]You[/bold blue]")
            
            if question.lower() in ['exit', 'quit', 'q']:
                console.print("👋 Goodbye!")
                break
            elif question.lower() == 'help':
                console.print("\n💡 [bold yellow]Suggested questions:[/bold yellow]")
                for i, suggestion in enumerate(suggestions, 1):
                    console.print(f"  {i}. {suggestion}")
                continue
            
            with console.status("🤖 AI is analyzing..."):
                response = cli.chat_with_ai(question)
            
            if "error" in response:
                console.print(f"❌ [red]Error: {response['error']}[/red]")
            else:
                console.print(f"\n🤖 [bold green]AI Assistant:[/bold green] {response.get('answer', 'No response')}")
                
        except KeyboardInterrupt:
            console.print("\n👋 Chat interrupted. Goodbye!")
            break

def cmd_analyze(cli: CyberDefenseCLI, args):
    """Get AI threat analysis"""
    console.print(f"\n🔍 [bold cyan]Analyzing threats from the last {args.hours} hours...[/bold cyan]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Running AI analysis...", total=None)
        analysis = cli.get_analysis(hours_back=args.hours)
    
    if "error" in analysis:
        console.print(f"❌ [red]Analysis failed: {analysis['error']}[/red]")
        return
    
    # Display analysis results
    panel = Panel(
        analysis.get('summary', 'No analysis available'),
        title="🧠 AI Threat Analysis",
        border_style="yellow"
    )
    console.print(panel)
    
    # Show recommendations if available
    if 'recommendations' in analysis:
        console.print("\n💡 [bold yellow]Recommendations:[/bold yellow]")
        recommendations = analysis['recommendations']
        if isinstance(recommendations, list):
            for i, rec in enumerate(recommendations, 1):
                console.print(f"  {i}. {rec}")
        else:
            console.print(f"  {recommendations}")

def cmd_stats(cli: CyberDefenseCLI, args):
    """Display system statistics"""
    console.print("\n📈 [bold cyan]Fetching system statistics...[/bold cyan]")
    
    with console.status("Calculating stats..."):
        stats = cli.get_stats()
    
    if "error" in stats:
        console.print(f"❌ [red]Stats unavailable: {stats['error']}[/red]")
        return
    
    # Create stats table
    table = Table(title="📊 System Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="center", style="bold")
    table.add_column("Details", style="dim")
    
    table.add_row("Total Logs", str(stats.get('total_logs', 0)), "All security events")
    table.add_row("Critical Events", f"[red]{stats.get('critical_count', 0)}[/red]", "Highest severity")
    table.add_row("High Severity", f"[yellow]{stats.get('high_count', 0)}[/yellow]", "High priority events")
    table.add_row("Medium Severity", f"[green]{stats.get('medium_count', 0)}[/green]", "Medium priority events")
    table.add_row("Low Severity", f"[blue]{stats.get('low_count', 0)}[/blue]", "Low priority events")
    
    if 'top_source_ips' in stats:
        top_ips = stats['top_source_ips'][:3]
        ips_text = ", ".join([f"{ip['source_ip']} ({ip['count']})" for ip in top_ips])
        table.add_row("Top Source IPs", ips_text, "Most active sources")
    
    console.print(table)

def cmd_monitor(cli: CyberDefenseCLI, args):
    """Real-time monitoring"""
    console.print("🔄 [bold cyan]Starting real-time monitoring...[/bold cyan]")
    console.print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Get recent logs
            logs = cli.get_logs(limit=5)
            stats = cli.get_stats()
            
            # Clear screen and show current time
            os.system('clear')
            console.print(f"🛡️ [bold cyan]Cyber Defense Monitor[/bold cyan] - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            console.print("=" * 60)
            
            # Show stats
            if "error" not in stats:
                console.print(f"📊 Total: {stats.get('total_logs', 0)} | "
                            f"[red]Critical: {stats.get('critical_count', 0)}[/red] | "
                            f"[yellow]High: {stats.get('high_count', 0)}[/yellow] | "
                            f"[green]Medium: {stats.get('medium_count', 0)}[/green]")
            
            console.print("\n🚨 [bold]Recent Events:[/bold]")
            for log in logs[:5]:
                timestamp = log.get('timestamp', '')[:19].replace('T', ' ')
                severity = log.get('severity', '')
                message = log.get('message', '')[:100]
                
                if severity == 'critical':
                    console.print(f"  {timestamp} | [bold red]CRITICAL[/bold red] | {message}")
                elif severity == 'high':
                    console.print(f"  {timestamp} | [red]HIGH[/red] | {message}")
                else:
                    console.print(f"  {timestamp} | [dim]{severity.upper()}[/dim] | {message}")
            
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        console.print("\n🛑 Monitoring stopped.")

def cmd_actions(cli: CyberDefenseCLI, args):
    """Execute security actions"""
    actions = {
        "block_ip": "Block IP Address",
        "isolate_host": "Isolate Host",
        "escalate_incident": "Escalate Incident", 
        "enable_monitoring": "Enable Enhanced Monitoring",
        "quarantine_file": "Quarantine File"
    }
    
    if not args.action:
        console.print("\n🛡️ [bold cyan]Available Security Actions:[/bold cyan]")
        for key, desc in actions.items():
            console.print(f"  {key} - {desc}")
        return
    
    if args.action not in actions:
        console.print(f"❌ Invalid action. Choose from: {', '.join(actions.keys())}")
        return
    
    if not args.target:
        target = Prompt.ask(f"Enter target for {actions[args.action]}")
    else:
        target = args.target
    
    console.print(f"\n🎯 [bold yellow]Executing: {actions[args.action]} on {target}[/bold yellow]")
    
    if not args.force:
        confirm = Confirm.ask(f"Are you sure you want to {args.action} {target}?")
        if not confirm:
            console.print("❌ Action cancelled")
            return
    
    with console.status("Executing action..."):
        result = cli.execute_action(args.action, target)
    
    if "error" in result:
        console.print(f"❌ [red]Action failed: {result['error']}[/red]")
    else:
        console.print(f"✅ [green]{result.get('message', 'Action completed successfully')}[/green]")
        if 'execution_id' in result:
            console.print(f"🆔 Execution ID: [cyan]{result['execution_id']}[/cyan]")

def cmd_demo(cli: CyberDefenseCLI, args):
    """Run demo scenarios"""
    scenarios = {
        "attack_sequence": "Run sequence of different attacks",
        "soc_incident": "Simulate SOC incident response",
        "threat_hunting": "Demonstrate threat hunting workflow"
    }
    
    if args.scenario == "attack_sequence":
        console.print("🚨 [bold red]Running Attack Sequence Demo...[/bold red]")
        attacks = ["ddos", "phishing", "insider_threat", "ransomware"]
        
        for i, attack in enumerate(attacks, 1):
            console.print(f"\n📍 Step {i}/4: Simulating {attack.replace('_', ' ').title()}...")
            result = cli.simulate_attack(attack)
            if "error" not in result:
                console.print(f"✅ {result['attack_type']} - {result['logs_created']} events created")
            time.sleep(2)
        
        console.print("\n🎯 [bold green]Attack sequence complete! Check the dashboard for results.[/bold green]")
    
    elif args.scenario == "soc_incident":
        console.print("🛡️ [bold cyan]SOC Incident Response Demo...[/bold cyan]")
        
        # 1. Generate incident
        console.print("\n1. Generating security incident...")
        result = cli.simulate_attack("ransomware")
        
        # 2. Get analysis
        console.print("2. Running AI analysis...")
        analysis = cli.get_analysis(hours_back=1)
        if "error" not in analysis:
            console.print("✅ Threat analysis complete")
        
        # 3. Show recommended actions
        console.print("3. Recommended actions:")
        console.print("   • Block malicious IPs")
        console.print("   • Isolate affected hosts") 
        console.print("   • Enable enhanced monitoring")
        
        console.print("\n🎯 [bold green]SOC workflow demonstrated![/bold green]")
    
    else:
        console.print("\n🎭 [bold cyan]Available Demo Scenarios:[/bold cyan]")
        for key, desc in scenarios.items():
            console.print(f"  {key} - {desc}")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="🛡️ Cyber Defense Assistant CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 cyber_defense_cli.py status
  python3 cyber_defense_cli.py simulate --type ddos --show-logs
  python3 cyber_defense_cli.py chat --message "What attacks happened today?"
  python3 cyber_defense_cli.py logs --limit 20 --severity critical
  python3 cyber_defense_cli.py monitor --interval 5
  python3 cyber_defense_cli.py actions --action block_ip --target 203.0.113.42
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Check system status')
    
    # Simulate command
    sim_parser = subparsers.add_parser('simulate', help='Run attack simulations')
    sim_parser.add_argument('--type', choices=['ddos', 'phishing', 'insider_threat', 'ransomware'],
                           help='Attack type to simulate')
    sim_parser.add_argument('--show-logs', action='store_true', help='Show recent logs after simulation')
    
    # Logs command
    logs_parser = subparsers.add_parser('logs', help='Display security logs')
    logs_parser.add_argument('--limit', type=int, default=10, help='Number of logs to show')
    logs_parser.add_argument('--severity', choices=['critical', 'high', 'medium', 'low'],
                            help='Filter by severity')
    logs_parser.add_argument('--export', action='store_true', help='Export logs to JSON file')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Chat with AI assistant')
    chat_parser.add_argument('--message', help='Single question to ask AI')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Get AI threat analysis')
    analyze_parser.add_argument('--hours', type=int, default=24, help='Hours back to analyze')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Display system statistics')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Real-time monitoring')
    monitor_parser.add_argument('--interval', type=int, default=10, help='Refresh interval in seconds')
    
    # Actions command
    actions_parser = subparsers.add_parser('actions', help='Execute security actions')
    actions_parser.add_argument('--action', choices=['block_ip', 'isolate_host', 'escalate_incident', 
                                                    'enable_monitoring', 'quarantine_file'],
                               help='Action to execute')
    actions_parser.add_argument('--target', help='Target for the action')
    actions_parser.add_argument('--force', action='store_true', help='Skip confirmation')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demo scenarios')
    demo_parser.add_argument('--scenario', choices=['attack_sequence', 'soc_incident', 'threat_hunting'],
                            help='Demo scenario to run')
    
    args = parser.parse_args()
    
    # Show help if no command provided
    if not args.command:
        parser.print_help()
        return
    
    # Initialize CLI
    cli = CyberDefenseCLI()
    
    # Route to appropriate command handler
    if args.command == 'status':
        cmd_status(cli, args)
    elif args.command == 'simulate':
        cmd_simulate(cli, args)
    elif args.command == 'logs':
        cmd_logs(cli, args)
    elif args.command == 'chat':
        cmd_chat(cli, args)
    elif args.command == 'analyze':
        cmd_analyze(cli, args)
    elif args.command == 'stats':
        cmd_stats(cli, args)
    elif args.command == 'monitor':
        cmd_monitor(cli, args)
    elif args.command == 'actions':
        cmd_actions(cli, args)
    elif args.command == 'demo':
        cmd_demo(cli, args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
