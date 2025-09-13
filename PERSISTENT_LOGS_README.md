# 🛡️ Cyber Defense Assistant - Persistent Demo Logs Setup

## Overview

The Cyber Defense Assistant now features **persistent demo logs** that are automatically stored in the SQLite database and displayed consistently every time you open the application. The "Generate Log" button adds new logs to this existing set.

## ✅ Current Status

### Database Configuration
- **Database Type**: SQLite (`cyber_defense.db`)
- **Persistent Demo Logs**: ✅ Automatically initialized
- **Total Logs**: 167+ (including historical and demo data)
- **Demo Log Marker**: `PERSISTENT_DEMO` (used to identify persistent logs)

### Log Categories
- 🔴 **Critical**: 37+ logs (Zero-day exploits, Nation-state actors, Ransomware)
- 🟠 **High**: 63+ logs (Advanced malware, SQL injection, Insider threats)
- 🟡 **Medium**: 50+ logs (Phishing, Firewall alerts, Policy violations)
- 🟢 **Low**: 17+ logs (Routine scans, System updates, Successful authentication)

## 🚀 How It Works

### 1. Automatic Initialization
When you start the backend server (`python3 main.py`), the system:
- Checks if persistent demo logs exist in the database
- If fewer than 5 demo logs are found, automatically creates a comprehensive set
- Displays a message confirming the demo logs are ready

### 2. Persistent Demo Logs
The system creates realistic military-themed security logs including:

**Critical Threats:**
- Zero-Day Exploit targeting military infrastructure
- Nation-State Actor (APT29) with sophisticated persistence
- Ransomware Attack targeting classified systems

**High Severity Events:**
- Advanced Malware with anti-analysis capabilities
- SQL Injection Attack on personnel database

**Medium Severity Events:**
- Spear Phishing Campaign against military personnel

**Low Severity Events:**
- Routine System Security Scans

### 3. Generate Log Button
The "Generate Log" button now creates more realistic logs with:
- **Varied Event Types**: Malware Detection, Network Intrusion, Phishing, etc.
- **Realistic IP Addresses**: Mix of internal and external IPs
- **Contextual Messages**: Military-themed, scenario-specific messages
- **Proper Severity Distribution**: Based on threat level

## 📊 Database Schema

```sql
Table: security_logs
- id: Primary key (auto-increment)
- timestamp: DateTime (UTC)
- source_ip: String (45 chars, supports IPv6)
- dest_ip: String (45 chars)
- event_type: String (100 chars, indexed)
- severity: String (20 chars, indexed) - 'low', 'medium', 'high', 'critical'
- message: Text (detailed event description)
```

## 🔧 Management Scripts

### `init_database.py`
Comprehensive database initialization with 20+ varied demo logs:
```bash
python3 init_database.py
```

### `create_demo_logs.py`
Creates focused set of essential demo logs:
```bash
python3 create_demo_logs.py
```

### Quick Status Check
```bash
python3 -c "
from database import SecurityLog
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

engine = create_engine('sqlite:///./cyber_defense.db')
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

demo_count = db.query(SecurityLog).filter(SecurityLog.message.like('%PERSISTENT_DEMO%')).count()
total_count = db.query(SecurityLog).count()
critical_count = db.query(SecurityLog).filter(SecurityLog.severity == 'critical').count()

print(f'Persistent Demo Logs: {demo_count}')
print(f'Total Logs: {total_count}')
print(f'Critical Threats: {critical_count}')

db.close()
"
```

## 🎯 Key Features

### ✅ Persistent Storage
- Logs survive application restarts
- Consistent dashboard appearance
- No need to regenerate data

### ✅ Realistic Data
- Military-themed scenarios
- Proper IP address ranges
- Contextual threat descriptions
- Varied severity levels

### ✅ Smart Generation
- "Generate Log" creates realistic new entries
- Adds to existing persistent set
- Uses proper templates and scenarios

### ✅ Dashboard Integration
- All tabs show consistent data
- Charts and graphs populate correctly
- AI analysis works with persistent logs

## 🌐 Access URLs

- **Frontend**: http://localhost:3002
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🚦 Starting the System

### 1. Start Backend (with auto-initialization)
```bash
cd "/Users/majjipradeepkumar/Downloads/haazri/cyber defence"
python3 main.py
```
*Output should show: "✅ Found X existing demo logs"*

### 2. Start Frontend
```bash
cd "/Users/majjipradeepkumar/Downloads/haazri/cyber defence/frontend"
npm start
```
*Will start on port 3002 if 3000 is in use*

## 📝 Demo Scenarios

The persistent logs include realistic military cybersecurity scenarios:

1. **Advanced Persistent Threat (APT)** - Nation-state actor targeting military systems
2. **Insider Threat Detection** - Employee accessing classified files outside hours  
3. **Ransomware Prevention** - Encryption attempts on classified systems blocked
4. **SQL Injection Defense** - Database attacks targeting personnel records
5. **Phishing Campaign** - Social engineering with military-specific content
6. **Network Intrusion** - Lateral movement across secured network segments
7. **Routine Operations** - Normal security scans and system monitoring

## 🎖️ Military-Grade Features

- **Classification Levels**: Handles classified data scenarios
- **Military Terminology**: Unit-specific, clearance-based language
- **Threat Intelligence**: Nation-state actors, APT groups
- **Operational Security**: Realistic military network topologies
- **Compliance**: Military security standards and protocols

---

**Status**: ✅ **FULLY OPERATIONAL**  
**Last Updated**: September 13, 2025  
**Demo Logs**: Persistent and Ready  
**Generate Feature**: Enhanced and Realistic
