# 🛡️ **CYBER DEFENSE CLI - INTERACTIVE DEMO & CHEAT SHEET**

## 🚀 **HOW TO INTERACT WITH THE CLI**

### **1. BASIC COMMAND STRUCTURE**
```bash
python3 cyber_defense_cli.py [COMMAND] [OPTIONS]
```

---

## 📋 **COMMAND REFERENCE**

### **🔍 System Management**
```bash
# Check system status
python3 cyber_defense_cli.py status

# View system statistics  
python3 cyber_defense_cli.py stats

# Real-time monitoring (Ctrl+C to stop)
python3 cyber_defense_cli.py monitor --interval 5
```

### **🚨 Attack Simulation**
```bash
# Interactive attack selection
python3 cyber_defense_cli.py simulate

# Specific attack types
python3 cyber_defense_cli.py simulate --type ddos --show-logs
python3 cyber_defense_cli.py simulate --type phishing --show-logs
python3 cyber_defense_cli.py simulate --type insider_threat --show-logs
python3 cyber_defense_cli.py simulate --type ransomware --show-logs
```

### **📊 Log Management**
```bash
# View recent logs
python3 cyber_defense_cli.py logs --limit 10

# Filter by severity
python3 cyber_defense_cli.py logs --severity critical --limit 20
python3 cyber_defense_cli.py logs --severity high --limit 15

# Export logs to JSON
python3 cyber_defense_cli.py logs --limit 100 --export
```

### **🤖 AI Assistant**
```bash
# Single question
python3 cyber_defense_cli.py chat --message "What attacks are happening?"

# Interactive chat mode
python3 cyber_defense_cli.py chat

# Threat analysis
python3 cyber_defense_cli.py analyze --hours 24
python3 cyber_defense_cli.py analyze --hours 1
```

### **🛡️ Security Actions**
```bash
# List available actions
python3 cyber_defense_cli.py actions

# Execute with confirmation
python3 cyber_defense_cli.py actions --action block_ip --target "203.0.113.42"

# Force execute without confirmation
python3 cyber_defense_cli.py actions --action block_ip --target "192.168.1.100" --force

# Other actions
python3 cyber_defense_cli.py actions --action isolate_host --target "workstation-01" --force
python3 cyber_defense_cli.py actions --action escalate_incident --target "INC-2024-001" --force
```

### **🎭 Demo Scenarios**
```bash
# List demo scenarios
python3 cyber_defense_cli.py demo

# Run attack sequence
python3 cyber_defense_cli.py demo --scenario attack_sequence

# SOC incident response demo
python3 cyber_defense_cli.py demo --scenario soc_incident
```

---

## 💡 **PRACTICAL USAGE PATTERNS**

### **🌅 Daily SOC Operations**
```bash
# Morning briefing routine
python3 cyber_defense_cli.py status
python3 cyber_defense_cli.py stats
python3 cyber_defense_cli.py logs --severity critical --limit 10
python3 cyber_defense_cli.py analyze --hours 24
python3 cyber_defense_cli.py chat --message "What's the current threat level?"
```

### **🚨 Incident Response**
```bash
# Emergency response workflow
python3 cyber_defense_cli.py logs --severity critical --limit 20
python3 cyber_defense_cli.py chat --message "What attacks are currently happening?"
python3 cyber_defense_cli.py analyze --hours 2
python3 cyber_defense_cli.py actions --action block_ip --target "MALICIOUS_IP" --force
python3 cyber_defense_cli.py logs --export  # Export evidence
```

### **🎓 Training & Demo Sessions**
```bash
# Complete demo sequence
python3 cyber_defense_cli.py demo --scenario attack_sequence
python3 cyber_defense_cli.py monitor --interval 3  # Watch in real-time
python3 cyber_defense_cli.py chat  # Interactive AI discussion
```

### **🔍 Threat Investigation**
```bash
# Investigate specific threats
python3 cyber_defense_cli.py logs --severity high --limit 50
python3 cyber_defense_cli.py chat --message "Analyze the IP 203.0.113.45"
python3 cyber_defense_cli.py chat --message "What should I do about ransomware?"
python3 cyber_defense_cli.py analyze --hours 6
```

---

## 🆘 **GETTING HELP**

### **General Help**
```bash
python3 cyber_defense_cli.py --help
```

### **Command-Specific Help**
```bash
python3 cyber_defense_cli.py simulate --help
python3 cyber_defense_cli.py logs --help
python3 cyber_defense_cli.py actions --help
python3 cyber_defense_cli.py chat --help
python3 cyber_defense_cli.py monitor --help
```

---

## 🎯 **INTERACTIVE EXAMPLES**

### **Example 1: Quick Threat Check**
```bash
$ python3 cyber_defense_cli.py status
$ python3 cyber_defense_cli.py chat --message "Any critical threats?"
```

### **Example 2: Simulate and Respond**
```bash
$ python3 cyber_defense_cli.py simulate --type ddos --show-logs
$ python3 cyber_defense_cli.py actions --action block_ip --target "203.0.113.45" --force
```

### **Example 3: Investigation Workflow**
```bash
$ python3 cyber_defense_cli.py logs --severity critical
$ python3 cyber_defense_cli.py analyze --hours 1
$ python3 cyber_defense_cli.py chat --message "What do these critical events mean?"
```

---

## 🔄 **MONITORING MODE**

### **Start Real-time Monitoring**
```bash
# Start monitoring with 5-second refresh
python3 cyber_defense_cli.py monitor --interval 5

# Press Ctrl+C to stop monitoring
```

**What you'll see in monitoring mode:**
- Live system statistics
- Recent security events  
- Color-coded severity levels
- Real-time timestamp updates

---

## 🎪 **INTERACTIVE CHAT MODE**

### **Starting Interactive Chat**
```bash
python3 cyber_defense_cli.py chat
```

**Chat Commands:**
- `help` - Show suggested questions
- `exit` or `quit` - Exit chat mode
- Type any security-related question

**Example Chat Questions:**
- "What attacks are happening?"
- "Should I be worried about 203.0.113.45?"
- "Analyze the recent ransomware events"
- "What's the most dangerous IP right now?"
- "How severe is the current threat level?"

---

## 📁 **FILE EXPORTS**

### **Export Security Logs**
```bash
# Export recent logs to JSON
python3 cyber_defense_cli.py logs --limit 100 --export

# Export critical events only
python3 cyber_defense_cli.py logs --severity critical --limit 50 --export
```

**Export files are automatically named with timestamp:**
- `security_logs_YYYYMMDD_HHMMSS.json`

---

## 🚀 **QUICK START DEMO SCRIPT**

### **Run Complete Demo**
```bash
# Quick comprehensive demo
./quick_cli_demo.sh

# Or step by step:
python3 cyber_defense_cli.py status
python3 cyber_defense_cli.py simulate --type ddos --show-logs  
python3 cyber_defense_cli.py stats
python3 cyber_defense_cli.py chat --message "What just happened?"
python3 cyber_defense_cli.py actions --action block_ip --target "203.0.113.45" --force
```

---

## ⚡ **PRO TIPS**

### **1. Batch Operations**
```bash
# Chain commands with &&
python3 cyber_defense_cli.py simulate --type ddos && python3 cyber_defense_cli.py stats
```

### **2. Output Formatting**
- CLI uses Rich library for beautiful colored output
- Tables are automatically formatted and responsive
- Progress bars show for long operations

### **3. Error Handling**
- CLI gracefully handles offline services
- Clear error messages with suggestions
- Timeout protection for network calls

### **4. Force Mode**
- Use `--force` flag to skip confirmations
- Useful for automation and scripting
- Be careful with destructive actions

---

## 🎯 **READY TO USE!**

**Start with these commands:**
1. `python3 cyber_defense_cli.py status` - Check system
2. `python3 cyber_defense_cli.py simulate --type ddos` - Run simulation  
3. `python3 cyber_defense_cli.py chat` - Talk to AI
4. `python3 cyber_defense_cli.py monitor` - Watch live activity

**The CLI provides complete command-line access to your entire cyber defense system!** 🚀
