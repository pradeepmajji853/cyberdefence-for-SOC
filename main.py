from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta, timezone
import os
import random
import json
from dotenv import load_dotenv

from database import get_db, SecurityLog, Base, engine
from models import LogEntry, LogResponse, AnalysisResponse, ChatRequest, ChatResponse
from ai_analyzer import AIAnalyzer

load_dotenv()

def initialize_demo_data():
    """Initialize persistent demo data if it doesn't exist"""
    try:
        # Import SessionLocal here to avoid circular imports
        from database import SessionLocal
        db = SessionLocal()
        
        # Check if demo logs exist
        demo_marker = "PERSISTENT_DEMO"
        existing_count = db.query(SecurityLog).filter(SecurityLog.message.like(f"%{demo_marker}%")).count()
        
        if existing_count < 5:  # Ensure we have at least 5 demo logs
            print("🔄 Initializing persistent demo logs...")
            
            # Clear old demo logs
            db.query(SecurityLog).filter(SecurityLog.message.like(f"%{demo_marker}%")).delete()
            
            # Create essential demo logs
            demo_logs = [
                {
                    "event_type": "Critical System Breach",
                    "severity": "critical",
                    "source_ip": "203.0.113.45",
                    "dest_ip": "192.168.1.100",
                    "message": f"Unauthorized root access detected on military server. Multiple authentication bypasses observed. [{demo_marker}]",
                    "minutes_ago": 15
                },
                {
                    "event_type": "Ransomware Detection",
                    "severity": "critical",
                    "source_ip": "192.168.1.65",
                    "dest_ip": "192.168.1.0/24",
                    "message": f"Advanced ransomware targeting classified systems. File encryption prevented by security measures. [{demo_marker}]",
                    "minutes_ago": 45
                },
                {
                    "event_type": "SQL Injection Attack",
                    "severity": "high",
                    "source_ip": "93.184.216.34",
                    "dest_ip": "192.168.1.100",
                    "message": f"Sophisticated SQL injection targeting personnel database. 127 malicious queries blocked. [{demo_marker}]",
                    "minutes_ago": 120
                },
                {
                    "event_type": "Spear Phishing Campaign",
                    "severity": "medium",
                    "source_ip": "172.16.254.78",
                    "dest_ip": "192.168.1.150",
                    "message": f"Targeted phishing campaign against military personnel. Social engineering with unit-specific details. [{demo_marker}]",
                    "minutes_ago": 240
                },
                {
                    "event_type": "System Security Scan",
                    "severity": "low",
                    "source_ip": "192.168.1.10",
                    "dest_ip": "N/A",
                    "message": f"Routine security scan completed successfully. All network components secure and operational. [{demo_marker}]",
                    "minutes_ago": 480
                }
            ]
            
            for log_data in demo_logs:
                timestamp = datetime.now(timezone.utc) - timedelta(minutes=log_data['minutes_ago'])
                
                db_log = SecurityLog(
                    timestamp=timestamp,
                    source_ip=log_data['source_ip'],
                    dest_ip=log_data['dest_ip'],
                    event_type=log_data['event_type'],
                    severity=log_data['severity'],
                    message=log_data['message']
                )
                
                db.add(db_log)
            
            db.commit()
            print(f"✅ Initialized {len(demo_logs)} persistent demo logs")
        else:
            print(f"✅ Found {existing_count} existing demo logs")
        
        db.close()
        
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize demo data: {e}")

# Create tables and initialize demo data
Base.metadata.create_all(bind=engine)
initialize_demo_data()

app = FastAPI(
    title="AI-Powered Cyber Defense Assistant",
    description="Military SOC Dashboard with AI-powered log analysis and chatbot",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI analyzer
ai_analyzer = AIAnalyzer()

@app.get("/")
async def root():
    return {"message": "AI-Powered Cyber Defense Assistant API", "status": "operational"}

@app.post("/logs", response_model=dict)
async def create_log(log_entry: LogEntry, db: Session = Depends(get_db)):
    """
    Accept and store security logs in the database.
    """
    try:
        db_log = SecurityLog(
            timestamp=log_entry.timestamp,
            source_ip=log_entry.source_ip,
            dest_ip=log_entry.dest_ip,
            event_type=log_entry.event_type,
            severity=log_entry.severity.lower(),
            message=log_entry.message
        )
        
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        
        return {"message": "Log entry created successfully", "id": db_log.id, "status": "success"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create log entry: {str(e)}")

@app.get("/logs", response_model=List[LogResponse])
async def get_logs(
    limit: int = 100,
    severity: Optional[str] = None,
    event_type: Optional[str] = None,
    hours_back: int = 24,
    db: Session = Depends(get_db)
):
    """
    Retrieve recent security logs with optional filtering.
    """
    try:
        query = db.query(SecurityLog)
        
        # Filter by time window
        since_time = datetime.utcnow() - timedelta(hours=hours_back)
        query = query.filter(SecurityLog.timestamp >= since_time)
        
        # Apply filters
        if severity:
            query = query.filter(SecurityLog.severity == severity.lower())
        if event_type:
            query = query.filter(SecurityLog.event_type.ilike(f"%{event_type}%"))
        
        # Order by most recent first and limit results
        logs = query.order_by(SecurityLog.timestamp.desc()).limit(limit).all()
        
        return [LogResponse(**log.to_dict()) for log in logs]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve logs: {str(e)}")

@app.get("/analysis", response_model=AnalysisResponse)
async def get_analysis(
    hours_back: int = 168,  # Default to 7 days (168 hours) to get all logs
    limit: int = 200,       # Analyze up to 200 logs for comprehensive analysis
    db: Session = Depends(get_db)
):
    """
    Analyze logs using Gemini AI to provide comprehensive threat summary, severity classification,
    and actionable recommendations. Analyzes ALL available logs by default.
    """
    try:
        # Fetch logs for analysis - get all logs if hours_back is large enough
        since_time = datetime.utcnow() - timedelta(hours=hours_back)
        logs = db.query(SecurityLog).filter(
            SecurityLog.timestamp >= since_time
        ).order_by(SecurityLog.timestamp.desc()).limit(limit).all()
        
        # If we don't get enough logs with time filter, get all logs
        if len(logs) < 50:
            logs = db.query(SecurityLog).order_by(SecurityLog.timestamp.desc()).limit(limit).all()
        
        # Convert to dict format for AI analysis
        log_dicts = [log.to_dict() for log in logs]
        
        # Get AI analysis
        analysis_result = ai_analyzer.analyze_logs(log_dicts)
        
        return AnalysisResponse(**analysis_result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    chat_request: ChatRequest,
    hours_back: int = 168,  # Default to 7 days to get all logs
    limit: int = 150,       # Increase context for better chat responses
    db: Session = Depends(get_db)
):
    """
    Natural language chat interface for SOC analysts to ask questions about logs.
    Uses comprehensive log context for better responses.
    """
    try:
        # Get logs for context - try time-based first
        since_time = datetime.utcnow() - timedelta(hours=hours_back)
        logs = db.query(SecurityLog).filter(
            SecurityLog.timestamp >= since_time
        ).order_by(SecurityLog.timestamp.desc()).limit(limit).all()
        
        # If we don't get enough logs with time filter, get all available logs
        if len(logs) < 50:
            logs = db.query(SecurityLog).order_by(SecurityLog.timestamp.desc()).limit(limit).all()
        
        log_dicts = [log.to_dict() for log in logs]
        
        # Get AI response
        ai_response = ai_analyzer.chat_response(chat_request.question, log_dicts)
        
        return ChatResponse(
            question=chat_request.question,
            answer=ai_response,
            context_logs_used=len(log_dicts)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get basic statistics about the security logs."""
    try:
        total_logs = db.query(SecurityLog).count()
        
        # Get counts by severity (last 24 hours)
        since_24h = datetime.utcnow() - timedelta(hours=24)
        recent_logs = db.query(SecurityLog).filter(SecurityLog.timestamp >= since_24h)
        
        severity_stats = {}
        for severity in ['low', 'medium', 'high', 'critical']:
            count = recent_logs.filter(SecurityLog.severity == severity).count()
            severity_stats[severity] = count
        
        # Top event types (last 24 hours)
        from sqlalchemy import func
        top_events = db.query(
            SecurityLog.event_type,
            func.count(SecurityLog.event_type).label('count')
        ).filter(
            SecurityLog.timestamp >= since_24h
        ).group_by(SecurityLog.event_type).order_by(
            func.count(SecurityLog.event_type).desc()
        ).limit(10).all()
        
        return {
            "total_logs": total_logs,
            "last_24h_severity": severity_stats,
            "top_event_types_24h": [{"event_type": event[0], "count": event[1]} for event in top_events],
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")

@app.post("/simulate-attack")
async def simulate_attack(attack_type: str, db: Session = Depends(get_db)):
    """Simulate various cyber attack scenarios for demo purposes"""
    try:
        attack_scenarios = {
            "ddos": {
                "name": "DDoS Attack",
                "severity": "critical",
                "logs": [
                    {"source_ip": "203.0.113.45", "message": "High volume traffic detected from malicious IP", "event_type": "DDoS Attack"},
                    {"source_ip": "198.51.100.32", "message": "Network congestion threshold exceeded", "event_type": "Network Overload"},
                    {"source_ip": "203.0.113.67", "message": "Coordinated botnet attack identified", "event_type": "Botnet Activity"}
                ]
            },
            "phishing": {
                "name": "Phishing Campaign",
                "severity": "high",
                "logs": [
                    {"source_ip": "192.0.2.44", "message": "Suspicious email with malicious attachment detected", "event_type": "Phishing Attempt"},
                    {"source_ip": "Internal", "message": "User clicked suspicious link - credential harvesting attempt", "event_type": "Social Engineering"},
                    {"source_ip": "192.0.2.44", "message": "Domain spoofing detected in email header", "event_type": "Domain Spoofing"}
                ]
            },
            "insider_threat": {
                "name": "Insider Threat",
                "severity": "critical",
                "logs": [
                    {"source_ip": "192.168.1.45", "message": "Unusual data access pattern by privileged user", "event_type": "Insider Threat"},
                    {"source_ip": "192.168.1.45", "message": "Large file download outside business hours", "event_type": "Data Exfiltration"},
                    {"source_ip": "192.168.1.45", "message": "Access attempt to restricted military database", "event_type": "Unauthorized Access"}
                ]
            },
            "ransomware": {
                "name": "Ransomware Attack",
                "severity": "critical",
                "logs": [
                    {"source_ip": "203.0.113.88", "message": "File encryption behavior detected on endpoint", "event_type": "Ransomware"},
                    {"source_ip": "203.0.113.88", "message": "Lateral movement across network shares", "event_type": "Network Propagation"},
                    {"source_ip": "203.0.113.88", "message": "Backup systems targeted for deletion", "event_type": "Backup Compromise"}
                ]
            }
        }
        
        if attack_type not in attack_scenarios:
            raise HTTPException(status_code=400, detail="Invalid attack type")
        
        scenario = attack_scenarios[attack_type]
        created_logs = []
        
        # Generate attack logs
        for i, log_data in enumerate(scenario["logs"]):
            log_entry = SecurityLog(
                event_type=log_data["event_type"],
                severity=scenario["severity"],
                source_ip=log_data["source_ip"],
                dest_ip="192.168.1.0/24",
                message=f"🚨 SIMULATED ATTACK: {log_data['message']} [DEMO]",
                timestamp=datetime.utcnow() - timedelta(seconds=i*30)
            )
            db.add(log_entry)
            created_logs.append(log_entry)
        
        db.commit()
        
        return {
            "status": "success",
            "attack_type": scenario["name"],
            "logs_created": len(created_logs),
            "message": f"Successfully simulated {scenario['name']} with {len(created_logs)} security events"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Attack simulation failed: {str(e)}")

@app.get("/threat-intelligence")
async def get_threat_intelligence():
    """Get simulated global threat intelligence data"""
    try:
        # Simulate real-time threat intelligence
        threat_feeds = [
            {
                "id": "THREAT-2024-001",
                "title": "APT29 Targeting Military Infrastructure",
                "severity": "critical",
                "region": "Southeast Asia",
                "description": "Nation-state malware variant targeting defense contractors",
                "indicators": ["203.0.113.0/24", "malware-c2.example.com"],
                "timestamp": datetime.utcnow().isoformat(),
                "confidence": "high"
            },
            {
                "id": "THREAT-2024-002", 
                "title": "Zero-Day Exploit in Defense Systems",
                "severity": "critical",
                "region": "Global",
                "description": "Critical vulnerability in military communication systems",
                "indicators": ["CVE-2024-XXXX", "Remote Code Execution"],
                "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
                "confidence": "confirmed"
            },
            {
                "id": "THREAT-2024-003",
                "title": "Ransomware Campaign Targeting Government",
                "severity": "high", 
                "region": "North America",
                "description": "Advanced ransomware with military-grade encryption",
                "indicators": ["198.51.100.0/24", "ransom-payment.onion"],
                "timestamp": (datetime.utcnow() - timedelta(hours=4)).isoformat(),
                "confidence": "medium"
            }
        ]
        
        return {
            "feeds": threat_feeds,
            "last_updated": datetime.utcnow().isoformat(),
            "total_threats": len(threat_feeds)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve threat intelligence: {str(e)}")

@app.get("/attack-map-data")
async def get_attack_map_data():
    """Get geographical data for attack visualization"""
    try:
        # Simulate real-time attack origins for world map
        attack_origins = [
            {"country": "China", "lat": 35.8617, "lng": 104.1954, "attacks": 45, "severity": "high"},
            {"country": "Russia", "lat": 61.5240, "lng": 105.3188, "attacks": 32, "severity": "critical"},
            {"country": "North Korea", "lat": 40.3399, "lng": 127.5101, "attacks": 28, "severity": "critical"},
            {"country": "Iran", "lat": 32.4279, "lng": 53.6880, "attacks": 23, "severity": "high"},
            {"country": "Unknown", "lat": 0, "lng": 0, "attacks": 67, "severity": "medium"},
            {"country": "Brazil", "lat": -14.2350, "lng": -51.9253, "attacks": 12, "severity": "low"},
            {"country": "Romania", "lat": 45.9432, "lng": 24.9668, "attacks": 8, "severity": "medium"}
        ]
        
        return {
            "origins": attack_origins,
            "timestamp": datetime.utcnow().isoformat(),
            "total_attacks": sum(origin["attacks"] for origin in attack_origins)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve attack map data: {str(e)}")

@app.post("/execute-action")
async def execute_security_action(action: str, target: str):
    """Execute automated security actions"""
    try:
        actions = {
            "block_ip": f"✅ IP Address {target} has been blocked at firewall level",
            "isolate_host": f"✅ Host {target} has been isolated from network",
            "escalate_incident": f"✅ Incident escalated to SOC Level 2 - Reference: INC-{random.randint(1000,9999)}",
            "enable_monitoring": f"✅ Enhanced monitoring enabled for {target}",
            "quarantine_file": f"✅ File {target} has been quarantined successfully"
        }
        
        if action not in actions:
            raise HTTPException(status_code=400, detail="Invalid action type")
            
        return {
            "status": "executed",
            "action": action,
            "target": target,
            "message": actions[action],
            "executed_at": datetime.utcnow().isoformat(),
            "execution_id": f"EXEC-{random.randint(10000,99999)}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Action execution failed: {str(e)}")

@app.get("/anomaly-detection")
async def get_anomaly_detection():
    """Get anomaly detection results"""
    try:
        anomalies = [
            {
                "id": "ANOMALY-001",
                "type": "Impossible Travel",
                "description": "User admin_miller logged in from India and 5 minutes later from Russia",
                "severity": "high",
                "user": "admin_miller",
                "locations": ["Mumbai, India", "Moscow, Russia"],
                "confidence": 0.95,
                "timestamp": datetime.utcnow().isoformat()
            },
            {
                "id": "ANOMALY-002", 
                "type": "Unusual Data Access",
                "description": "Database access pattern 300% above normal baseline",
                "severity": "medium",
                "user": "service_account_db",
                "baseline": "Normal: 150 queries/hour",
                "current": "Current: 450 queries/hour",
                "confidence": 0.87,
                "timestamp": (datetime.utcnow() - timedelta(minutes=15)).isoformat()
            },
            {
                "id": "ANOMALY-003",
                "type": "Off-Hours Activity",
                "description": "Critical system access during maintenance window",
                "severity": "medium",
                "user": "contractor_smith",
                "expected": "No access during 02:00-04:00 UTC",
                "confidence": 0.78,
                "timestamp": (datetime.utcnow() - timedelta(hours=1)).isoformat()
            }
        ]
        
        return {
            "anomalies": anomalies,
            "total_anomalies": len(anomalies),
            "last_scan": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve anomalies: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
