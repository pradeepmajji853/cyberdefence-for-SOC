#!/usr/bin/env python3
"""
🎯 Comprehensive CLI Demo Script
================================

This script demonstrates all CLI capabilities in a structured demo.
Perfect for presentations and training sessions.
"""

import subprocess
import time
import os
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

console = Console()

def run_cli_command(cmd, description=""):
    """Run a CLI command and display results"""
    if description:
        console.print(f"\n🔍 [bold cyan]{description}[/bold cyan]")
    
    console.print(f"[dim]$ {cmd}[/dim]")
    
    try:
        result = subprocess.run(
            cmd.split(),
            capture_output=True,
            text=True,
            cwd="/Users/majjipradeepkumar/Downloads/haazri/cyber defence"
        )
        
        if result.stdout:
            console.print(result.stdout)
        if result.stderr:
            console.print(f"[red]{result.stderr}[/red]")
            
        return result.returncode == 0
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return False

def demo_basic_cli():
    """Demo basic CLI functionality"""
    console.print(Panel("🛡️ Basic CLI Functionality Demo", style="cyan"))
    
    demos = [
        ("python3 cyber_defense_cli.py status", "System Status Check"),
        ("python3 cyber_defense_cli.py simulate --type ddos --show-logs", "DDoS Attack Simulation"),
        ("python3 cyber_defense_cli.py logs --limit 5 --severity critical", "View Critical Logs"),
        ("python3 cyber_defense_cli.py stats", "System Statistics"),
        ("python3 cyber_defense_cli.py chat --message 'What attacks are active?'", "AI Chat Query"),
        ("python3 cyber_defense_cli.py actions --action block_ip --target '203.0.113.42' --force", "Security Action"),
    ]
    
    for cmd, desc in demos:
        run_cli_command(cmd, desc)
        time.sleep(2)

def demo_attack_scenarios():
    """Demo various attack scenarios"""
    console.print(Panel("🚨 Attack Simulation Scenarios", style="red"))
    
    attacks = ["ddos", "phishing", "insider_threat", "ransomware"]
    
    for attack in track(attacks, description="Running attack simulations..."):
        run_cli_command(f"python3 cyber_defense_cli.py simulate --type {attack}", f"Simulating {attack.replace('_', ' ').title()}")
        time.sleep(1)
    
    # Show results
    run_cli_command("python3 cyber_defense_cli.py logs --limit 10", "Recent Attack Logs")

def demo_monitoring_workflow():
    """Demo monitoring and analysis workflow"""
    console.print(Panel("📊 SOC Monitoring Workflow", style="green"))
    
    workflow = [
        ("python3 cyber_defense_cli.py stats", "Current System Stats"),
        ("python3 cyber_defense_cli.py analyze --hours 1", "AI Threat Analysis"),
        ("python3 cyber_defense_cli.py chat --message 'What should I prioritize?'", "AI Recommendations"),
        ("python3 cyber_defense_cli.py logs --severity high --limit 5", "High Priority Events"),
    ]
    
    for cmd, desc in workflow:
        run_cli_command(cmd, desc)
        time.sleep(1)

def demo_incident_response():
    """Demo incident response workflow"""
    console.print(Panel("🚑 Incident Response Demo", style="yellow"))
    
    # 1. Generate incident
    run_cli_command("python3 cyber_defense_cli.py simulate --type ransomware", "⚠️ Ransomware Incident Detected")
    
    # 2. Immediate response
    incident_response = [
        ("python3 cyber_defense_cli.py logs --severity critical --limit 3", "🔍 Investigate Critical Events"),
        ("python3 cyber_defense_cli.py analyze --hours 1", "🧠 AI Analysis"),
        ("python3 cyber_defense_cli.py actions --action isolate_host --target 'infected-workstation' --force", "🛡️ Isolate Affected Host"),
        ("python3 cyber_defense_cli.py actions --action block_ip --target '203.0.113.88' --force", "🚫 Block Malicious IP"),
        ("python3 cyber_defense_cli.py chat --message 'What other actions should I take?'", "💡 Additional Recommendations"),
    ]
    
    for cmd, desc in incident_response:
        run_cli_command(cmd, desc)
        time.sleep(1)

def create_demo_report():
    """Create a comprehensive demo report"""
    console.print(Panel("📋 Generating Demo Report", style="blue"))
    
    # Export logs
    run_cli_command("python3 cyber_defense_cli.py logs --limit 50 --export", "📁 Export Security Logs")
    
    # Get final stats
    run_cli_command("python3 cyber_defense_cli.py stats", "📊 Final System Statistics")
    
    console.print("\n✅ [bold green]Demo completed successfully![/bold green]")
    console.print("📁 Check for exported files in the current directory")

def interactive_menu():
    """Interactive demo menu"""
    while True:
        console.print("\n" + "="*60)
        console.print("🛡️ [bold cyan]Cyber Defense CLI Demo Menu[/bold cyan]")
        console.print("="*60)
        
        options = {
            "1": ("Basic CLI Functionality", demo_basic_cli),
            "2": ("Attack Simulation Scenarios", demo_attack_scenarios),  
            "3": ("SOC Monitoring Workflow", demo_monitoring_workflow),
            "4": ("Incident Response Demo", demo_incident_response),
            "5": ("Full Demo Sequence", run_full_demo),
            "6": ("Generate Report", create_demo_report),
            "q": ("Quit", None)
        }
        
        for key, (desc, _) in options.items():
            console.print(f"  [cyan]{key}[/cyan]. {desc}")
        
        choice = console.input("\n[bold]Select an option: [/bold]").strip().lower()
        
        if choice == 'q':
            console.print("👋 [bold]Thanks for using the CLI demo![/bold]")
            break
        elif choice in options and options[choice][1]:
            options[choice][1]()
        else:
            console.print("❌ Invalid option. Please try again.")

def run_full_demo():
    """Run the complete demo sequence"""
    console.print(Panel("🚀 Running Complete CLI Demo Sequence", style="magenta"))
    
    demo_functions = [
        demo_basic_cli,
        demo_attack_scenarios,
        demo_monitoring_workflow,
        demo_incident_response,
        create_demo_report
    ]
    
    for demo_func in demo_functions:
        demo_func()
        console.print("\n" + "="*60)
        time.sleep(2)

def main():
    """Main demo script"""
    console.print("""
🛡️ [bold cyan]Welcome to the Cyber Defense CLI Demo![/bold cyan]

This demonstration showcases the comprehensive command-line interface 
for the AI-Powered Cyber Defense System.

Features demonstrated:
• System status monitoring
• Attack simulations  
• Security log management
• AI-powered threat analysis
• Incident response workflows
• Security action execution
• Real-time monitoring capabilities

""")
    
    # Quick system check
    console.print("🔍 [bold]Quick System Check...[/bold]")
    success = run_cli_command("python3 cyber_defense_cli.py status", "")
    
    if not success:
        console.print("❌ [red]System check failed. Please ensure backend is running.[/red]")
        console.print("Start backend with: [yellow]python3 main.py[/yellow]")
        return
    
    # Run interactive menu
    interactive_menu()

if __name__ == "__main__":
    main()
