from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class FraudLog(Base):
    """Table to store fraud analysis logs."""
    __tablename__ = "fraud_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    risk_score = Column(Integer)
    risk_level = Column(String)
    threat_category = Column(String)
    confidence = Column(Integer)
    timestamp = Column(DateTime, default=datetime.now)


class Blacklist(Base):
    """Table to store blacklisted phone numbers."""
    __tablename__ = "blacklist"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    reason = Column(String)
    added_at = Column(DateTime, default=datetime.now)
