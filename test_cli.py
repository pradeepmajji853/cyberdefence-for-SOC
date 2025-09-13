#!/usr/bin/env python3
"""
Simple test version of the CLI
"""

import requests
import json
from rich.console import Console
from rich.table import Table

console = Console()

def test_status():
    """Test system status"""
    console.print("🔍 [bold cyan]Testing Cyber Defense CLI...[/bold cyan]")
    
    try:
        # Test backend
        response = requests.get("http://localhost:8001/health", timeout=3)
        backend_ok = response.status_code == 200
        console.print(f"Backend: {'✅ Online' if backend_ok else '❌ Offline'}")
        
        # Test frontend  
        response = requests.get("http://localhost:3000", timeout=3)
        frontend_ok = response.status_code == 200
        console.print(f"Frontend: {'✅ Online' if frontend_ok else '❌ Offline'}")
        
    except Exception as e:
        console.print(f"Error: {e}")

if __name__ == "__main__":
    test_status()
