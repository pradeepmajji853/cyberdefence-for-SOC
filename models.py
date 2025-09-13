from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class LogEntry(BaseModel):
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    source_ip: str = Field(..., description="Source IP address")
    dest_ip: str = Field(..., description="Destination IP address")
    event_type: str = Field(..., description="Type of security event")
    severity: str = Field(..., description="Severity level: low, medium, high, critical")
    message: str = Field(..., description="Detailed event message")

class LogResponse(BaseModel):
    id: int
    timestamp: datetime
    source_ip: str
    dest_ip: str
    event_type: str
    severity: str
    message: str

class AnalysisResponse(BaseModel):
    summary: str
    threats_identified: List[str]
    severity_classification: str
    recommendations: List[str]
    total_logs_analyzed: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatRequest(BaseModel):
    question: str = Field(..., description="Natural language question about security logs")

class ChatResponse(BaseModel):
    question: str
    answer: str
    context_logs_used: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
