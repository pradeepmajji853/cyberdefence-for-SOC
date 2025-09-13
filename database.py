from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cyber_defense.db")

class SecurityLog(Base):
    __tablename__ = "security_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_ip = Column(String(45), index=True)  # IPv6 support
    dest_ip = Column(String(45), index=True)
    event_type = Column(String(100), index=True)
    severity = Column(String(20), index=True)  # low, medium, high, critical
    message = Column(Text)
    
    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "source_ip": self.source_ip,
            "dest_ip": self.dest_ip,
            "event_type": self.event_type,
            "severity": self.severity,
            "message": self.message
        }

# Database setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
