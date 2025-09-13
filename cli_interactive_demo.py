#!/usr/bin/env python3
"""
Demo script showing interactive CLI usage patterns
"""

import subprocess
import time
from rich.console import Console

console = Console()

def demonstrate_cli_commands():
    """Demonstrate various CLI command patterns"""
    
    console.print("\n🎯 [bold cyan]CLI COMMAND PATTERNS DEMO[/bold cyan]")
    console.print("=" * 50)
    
    # Command examples with descriptions
    commands = [
        {
            "title": "📊 View Recent Logs",
            "command": "python3 cyber_defense_cli.py logs --limit 10",
            "description": "Shows the 10 most recent security events"
        },
        {
            "title": "🚨 Simulate Phishing Attack",
            "command": "python3 cyber_defense_cli.py simulate --type phishing",
            "description": "Runs a phishing campaign simulation"
        },
        {
            "title": "🔍 Get AI Analysis",
            "command": "python3 cyber_defense_cli.py analyze --hours 1",
            "description": "AI analysis of threats from the last hour"
        },
        {
            "title": "🛡️ Block Suspicious IP", 
            "command": "python3 cyber_defense_cli.py actions --action block_ip --target '198.51.100.32' --force",
            "description": "Immediately block a suspicious IP address"
        }
    ]
    
    for cmd_info in commands:
        console.print(f"\n🔹 [bold yellow]{cmd_info['title']}[/bold yellow]")
        console.print(f"   {cmd_info['description']}")
        console.print(f"   [dim]Command: {cmd_info['command']}[/dim]")
    
    console.print(f"\n✨ [bold green]All commands are ready to use![/bold green]")

def show_cli_help_commands():
    """Show help for specific commands"""
    
    console.print("\n🆘 [bold cyan]GETTING HELP FOR SPECIFIC COMMANDS[/bold cyan]")
    console.print("=" * 50)
    
    help_commands = [
        "python3 cyber_defense_cli.py simulate --help",
        "python3 cyber_defense_cli.py logs --help", 
        "python3 cyber_defense_cli.py actions --help",
        "python3 cyber_defense_cli.py chat --help"
    ]
    
    for cmd in help_commands:
        console.print(f"📖 [cyan]{cmd}[/cyan]")

def show_useful_cli_patterns():
    """Show useful CLI usage patterns"""
    
    console.print("\n💡 [bold cyan]USEFUL CLI PATTERNS[/bold cyan]")
    console.print("=" * 50)
    
    patterns = [
        {
            "scenario": "🌅 Morning SOC Briefing",
            "commands": [
                "python3 cyber_defense_cli.py status",
                "python3 cyber_defense_cli.py stats", 
                "python3 cyber_defense_cli.py logs --severity critical --limit 5",
                "python3 cyber_defense_cli.py analyze --hours 24"
            ]
        },
        {
            "scenario": "🚨 Incident Response",
            "commands": [
                "python3 cyber_defense_cli.py logs --severity critical",
                "python3 cyber_defense_cli.py chat --message 'What attacks are happening?'",
                "python3 cyber_defense_cli.py actions --action block_ip --target 'MALICIOUS_IP'",
                "python3 cyber_defense_cli.py logs --export"
            ]
        },
        {
            "scenario": "🎓 Training & Demo",
            "commands": [
                "python3 cyber_defense_cli.py demo --scenario attack_sequence",
                "python3 cyber_defense_cli.py monitor --interval 3",
                "python3 cyber_defense_cli.py chat"
            ]
        }
    ]
    
    for pattern in patterns:
        console.print(f"\n🎯 [bold yellow]{pattern['scenario']}[/bold yellow]")
        for cmd in pattern['commands']:
            console.print(f"   [green]${cmd}[/green]")

if __name__ == "__main__":
    demonstrate_cli_commands()
    show_cli_help_commands() 
    show_useful_cli_patterns()
    
    console.print("\n🚀 [bold cyan]Ready to try the CLI? Start with:[/bold cyan]")
    console.print("   [green]python3 cyber_defense_cli.py status[/green]")
    console.print("\n📚 [bold]For full help:[/bold]")
    console.print("   [green]python3 cyber_defense_cli.py --help[/green]")
