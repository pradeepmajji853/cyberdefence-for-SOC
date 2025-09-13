from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta, timezone
import os
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
