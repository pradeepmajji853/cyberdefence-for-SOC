#!/bin/bash

# 🛡️ Cyber Defense CLI Quick Demo
echo "🛡️ Cyber Defense CLI - Quick Demonstration"
echo "=========================================="
echo ""

cd "/Users/majjipradeepkumar/Downloads/haazri/cyber defence"

echo "1️⃣ System Status Check:"
python3 cyber_defense_cli.py status
echo ""

echo "2️⃣ DDoS Attack Simulation:"
python3 cyber_defense_cli.py simulate --type ddos --show-logs
echo ""

echo "3️⃣ Current Statistics:"
python3 cyber_defense_cli.py stats
echo ""

echo "4️⃣ AI Chat Query:"
python3 cyber_defense_cli.py chat --message "What threats should I be concerned about?"
echo ""

echo "5️⃣ Security Action:"
python3 cyber_defense_cli.py actions --action block_ip --target "203.0.113.45" --force
echo ""

echo "✅ CLI Demo Complete!"
echo "Run 'python3 cyber_defense_cli.py --help' for all options"
