# 🛡️ Cyber Defense CLI - Complete Usage Guide

## 🚀 Basic CLI (cyber_defense_cli.py)

### Installation & Setup
```bash
# Make sure Rich library is installed
pip install rich requests

# Make CLI executable
chmod +x cyber_defense_cli.py
```

### Core Commands

#### 1. System Status
```bash
# Check if all services are running
python3 cyber_defense_cli.py status
```

#### 2. Attack Simulation
```bash
# Interactive attack selection
python3 cyber_defense_cli.py simulate

# Specific attack with logs
python3 cyber_defense_cli.py simulate --type ddos --show-logs
python3 cyber_defense_cli.py simulate --type phishing --show-logs
python3 cyber_defense_cli.py simulate --type insider_threat --show-logs
python3 cyber_defense_cli.py simulate --type ransomware --show-logs
```

#### 3. Security Logs Management
```bash
# View recent logs
python3 cyber_defense_cli.py logs --limit 10

# Filter by severity
python3 cyber_defense_cli.py logs --severity critical --limit 20

# Export logs to JSON
python3 cyber_defense_cli.py logs --limit 100 --export
```

#### 4. AI Chat Interface
```bash
# Single question
python3 cyber_defense_cli.py chat --message "What attacks happened today?"

# Interactive chat mode
python3 cyber_defense_cli.py chat
```

#### 5. Threat Analysis
```bash
# Analyze last 24 hours
python3 cyber_defense_cli.py analyze --hours 24

# Quick analysis
python3 cyber_defense_cli.py analyze --hours 1
```

#### 6. System Statistics
```bash
# View current stats
python3 cyber_defense_cli.py stats
```

#### 7. Security Actions
```bash
# List available actions
python3 cyber_defense_cli.py actions

# Execute actions (with confirmation)
python3 cyber_defense_cli.py actions --action block_ip --target "203.0.113.42"
python3 cyber_defense_cli.py actions --action isolate_host --target "workstation-01"

# Force execute without confirmation
python3 cyber_defense_cli.py actions --action block_ip --target "192.168.1.100" --force
```

#### 8. Real-time Monitoring
```bash
# Start monitoring (Ctrl+C to stop)
python3 cyber_defense_cli.py monitor

# Custom refresh interval
python3 cyber_defense_cli.py monitor --interval 3
```

#### 9. Demo Scenarios
```bash
# List demo scenarios
python3 cyber_defense_cli.py demo

# Run attack sequence demo
python3 cyber_defense_cli.py demo --scenario attack_sequence

# SOC incident response demo
python3 cyber_defense_cli.py demo --scenario soc_incident
```

---

## 🔥 Advanced CLI (advanced_cli.py)

### Enhanced Features

#### 1. Batch Attack Simulation
```bash
# Simulate multiple attacks in sequence
python3 advanced_cli.py batch-simulate ddos phishing ransomware

# With custom delay between attacks
python3 advanced_cli.py batch-simulate ddos insider_threat --delay 5
```

#### 2. Advanced Log Export
```bash
# Export to JSON with filters
python3 advanced_cli.py export-logs --format json --severity critical --hours 48

# Export to CSV
python3 advanced_cli.py export-logs --format csv --hours 24

# Export all logs
python3 advanced_cli.py export-logs --hours 168  # Last week
```

#### 3. System Health Report
```bash
# Generate comprehensive health report
python3 advanced_cli.py health-report
```

#### 4. Quick Setup & Test
```bash
# Complete system setup and test
python3 advanced_cli.py quick-setup
```

---

## 📋 Common Usage Patterns

### 1. Daily SOC Operations
```bash
# Morning routine
python3 cyber_defense_cli.py status
python3 cyber_defense_cli.py analyze --hours 24
python3 cyber_defense_cli.py logs --severity critical --limit 10

# Quick threat check
python3 cyber_defense_cli.py chat --message "What's the current threat level?"
```

### 2. Incident Response
```bash
# During an incident
python3 cyber_defense_cli.py logs --severity critical --limit 50
python3 cyber_defense_cli.py analyze --hours 2
python3 cyber_defense_cli.py actions --action block_ip --target "SUSPICIOUS_IP"

# Export evidence
python3 advanced_cli.py export-logs --format json --severity critical --hours 6
```

### 3. Demo & Training
```bash
# Full demo sequence
python3 cyber_defense_cli.py demo --scenario attack_sequence
python3 cyber_defense_cli.py monitor  # Watch in real-time
python3 cyber_defense_cli.py chat --message "Analyze the recent attacks"

# Batch testing
python3 advanced_cli.py batch-simulate ddos phishing insider_threat ransomware --delay 3
```

### 4. System Maintenance
```bash
# Health check
python3 advanced_cli.py health-report

# Export logs for archival
python3 advanced_cli.py export-logs --format csv --hours 168

# Clean demo after presentation
python3 cyber_defense_cli.py stats  # Check current state
```

---

## 🎯 Quick Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `status` | System health | `python3 cyber_defense_cli.py status` |
| `simulate` | Attack simulation | `python3 cyber_defense_cli.py simulate --type ddos` |
| `logs` | View security logs | `python3 cyber_defense_cli.py logs --limit 20` |
| `chat` | AI assistance | `python3 cyber_defense_cli.py chat` |
| `analyze` | Threat analysis | `python3 cyber_defense_cli.py analyze --hours 24` |
| `stats` | Statistics | `python3 cyber_defense_cli.py stats` |
| `actions` | Execute actions | `python3 cyber_defense_cli.py actions --action block_ip` |
| `monitor` | Real-time monitoring | `python3 cyber_defense_cli.py monitor` |
| `demo` | Demo scenarios | `python3 cyber_defense_cli.py demo --scenario attack_sequence` |

---

## 🔧 Configuration

The CLI automatically creates a `cli_config.json` file with default settings:

```json
{
  "api_url": "http://localhost:8001",
  "default_log_limit": 10,
  "monitor_interval": 5,
  "auto_refresh": true
}
```

## 🎪 Demo Script for Presentations

```bash
# 1. System status
python3 cyber_defense_cli.py status

# 2. Run demo attacks
python3 cyber_defense_cli.py demo --scenario attack_sequence

# 3. Check results
python3 cyber_defense_cli.py stats
python3 cyber_defense_cli.py logs --severity critical --limit 10

# 4. AI analysis
python3 cyber_defense_cli.py chat --message "What just happened? Analyze the attacks."

# 5. Take action
python3 cyber_defense_cli.py actions --action block_ip --target "203.0.113.45" --force

# 6. Export report
python3 advanced_cli.py export-logs --format json --hours 1
```

## 🚨 Troubleshooting

### Backend Not Running
```bash
# Check status first
python3 cyber_defense_cli.py status

# If backend is offline, start it:
python3 main.py
```

### No Logs Found
```bash
# Generate some demo data
python3 cyber_defense_cli.py simulate --type ddos
python3 cyber_defense_cli.py simulate --type phishing
```

### Permission Denied
```bash
# Make CLI executable
chmod +x cyber_defense_cli.py
chmod +x advanced_cli.py
```

---

**🎯 The CLI provides complete command-line access to all features of your cyber defense system!**
