from fastapi import FastAPI, Request, Depends, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models import FraudRequest, FraudResponse
from detection_engine import ScamDetectionEngine
from risk_scorer import RiskScorer
from explainable_ai import ExplainableAI
from phone_analyzer import PhoneAnalyzer
from ml_model import MLModel
from ip_analyzer import IPAnalyzer
from blacklist import BlacklistChecker
from rate_limiter import RateLimiter
from logger import FraudLogger
from history_store import HistoryStore
from datetime import datetime
from database import get_db, init_db
from db_models import FraudLog, Blacklist
from security import verify_api_key, verify_admin_key
from alert_service import AlertService
from config import config
from typing import List
import json

app = FastAPI(title="Cyber Fraud Detection System")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Initialize database and create tables on startup
init_db()

# Initialize all components once at startup
ml_model = MLModel()
ip_analyzer = IPAnalyzer()
blacklist_checker = BlacklistChecker()
rate_limiter = RateLimiter()
fraud_logger = FraudLogger()
history_store = HistoryStore()
alert_service = AlertService()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@app.get("/")
async def root():
    """Welcome endpoint - No authentication required."""
    return {
        "message": "Welcome to Cyber Fraud Detection System",
        "version": "2.0.0",
        "usage": "POST to /analyze with phone_number and/or message_content",
        "admin_dashboard": "/admin",
        "authentication": {
            "header": "X-API-KEY",
            "public_key": "Use PUBLIC_API_KEY environment variable (default: public123 for local dev)",
            "admin_key": "Use ADMIN_API_KEY environment variable (default: admin123 for local dev)"
        },
        "documentation": {
            "interactive": "/docs",
            "alternative": "/redoc"
        }
    }

@app.post("/analyze", response_model=FraudResponse)
async def analyze_message(
    fraud_request: FraudRequest, 
    request: Request, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Analyze a message for potential fraud indicators."""
    # Use message_content for analysis, default to empty string if not provided
    message = fraud_request.message_content or ""
    phone = fraud_request.phone_number or ""
    
    # Get client IP address
    client_ip = request.client.host if request.client else None
    
    # Step 1: Instantiate and detect fraud indicators
    detection_engine = ScamDetectionEngine()
    detection_results = detection_engine.analyze(message)
    
    # Step 1.5: Analyze phone number for suspicious patterns
    phone_analyzer = PhoneAnalyzer()
    phone_analysis = phone_analyzer.analyze(phone)
    
    # Step 2: Instantiate and calculate rule-based risk score (including phone analysis)
    risk_scorer = RiskScorer()
    risk_data = risk_scorer.calculate_score(detection_results, phone_analysis)
    rule_score = risk_data["score"]
    confidence = risk_data["confidence"]
    
    # Step 2.5: Get ML-based probability
    ml_probability = ml_model.predict_probability(message)
    
    # Step 2.6: Combine rule-based and ML-based scores
    final_score = int((rule_score * 0.6) + (ml_probability * 40))
    
    # Step 3: Apply additional risk adjustments
    additional_factors = []
    
    # IP analysis
    ip_result = ip_analyzer.analyze(client_ip)
    final_score += ip_result["risk_adjustment"]
    if ip_result["reason"]:
        additional_factors.append(ip_result["reason"])
    
    # Blacklist check
    blacklist_result = blacklist_checker.check(phone, message)
    final_score += blacklist_result["risk_boost"]
    if blacklist_result["reason"]:
        additional_factors.append(blacklist_result["reason"])
    
    # Rate limiting check
    rate_limit_result = rate_limiter.check(phone)
    final_score += rate_limit_result["risk_boost"]
    if rate_limit_result["reason"]:
        additional_factors.append(rate_limit_result["reason"])
    
    # History check - add risk if previously flagged
    history_result = history_store.check_previous_risk(phone)
    final_score += history_result["risk_boost"]
    if history_result["reason"]:
        additional_factors.append(history_result["reason"])
    
    # Cap final score at 100
    final_score = min(final_score, 100)
    
    # Determine risk level based on final score
    if final_score <= 30:
        risk_level = "Low"
    elif final_score <= 60:
        risk_level = "Medium"
    elif final_score <= 85:
        risk_level = "High"
    else:
        risk_level = "Critical"
    
    # Step 4: Instantiate and generate explanation
    explainable_ai = ExplainableAI()
    explanation_data = explainable_ai.generate_explanation(final_score, detection_results, phone_analysis)
    
    # Add additional factors to contributing factors
    all_contributing_factors = explanation_data["contributing_factors"] + additional_factors
    
    # Create simple explanation text for backward compatibility
    explanation = f"{risk_level} risk. {explanation_data['primary_reason']}"
    
    # Step 5: Log the result
    fraud_logger.log(phone, final_score, risk_level)
    
    # Step 6: Store in history (in-memory)
    history_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "phone_number": phone,
        "message_content": message[:100],  # Store first 100 chars
        "risk_score": final_score,
        "risk_level": risk_level,
        "confidence": confidence,
        "threat_category": explanation_data["threat_category"]
    }
    history_store.add(phone, history_entry)
    
    # Step 7: Save to database
    fraud_log = FraudLog(
        phone_number=phone,
        risk_score=final_score,
        risk_level=risk_level,
        threat_category=explanation_data["threat_category"],
        confidence=confidence,
        timestamp=datetime.now()
    )
    db.add(fraud_log)
    db.commit()
    
    # Step 8: Add to blacklist if Critical
    if risk_level == "Critical" and phone:
        # Check if already blacklisted
        existing = db.query(Blacklist).filter(Blacklist.phone_number == phone).first()
        if not existing:
            blacklist_entry = Blacklist(
                phone_number=phone,
                reason=f"Automatically blacklisted due to Critical risk: {explanation_data['primary_reason']}",
                added_at=datetime.now()
            )
            db.add(blacklist_entry)
            db.commit()
            
        # Send alerts in background
        background_tasks.add_task(
            alert_service.send_alert,
            phone_number=phone,
            risk_score=final_score,
            risk_level=risk_level,
            threat_category=explanation_data["threat_category"],
            primary_reason=explanation_data["primary_reason"]
        )
    
    # Step 9: Broadcast to WebSocket clients
    background_tasks.add_task(broadcast_update, db)
    
    return FraudResponse(
        risk_score=final_score,
        explanation=explanation,
        risk_level=risk_level,
        confidence=confidence,
        primary_reason=explanation_data["primary_reason"],
        contributing_factors=all_contributing_factors,
        recommendation=explanation_data["recommendation"],
        threat_category=explanation_data["threat_category"]
    )

@app.get("/")
async def root():
    """Welcome endpoint."""
    return {
        "message": "Welcome to Cyber Fraud Detection System",
        "usage": "POST to /analyze with phone_number and/or message_content",
        "admin_dashboard": "/admin"
    }

@app.get("/admin")
async def admin_dashboard(
    request: Request, 
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_admin_key)
):
    """Admin dashboard with statistics and visualizations - Admin only."""
    # Query statistics
    total_requests = db.query(FraudLog).count()
    critical_count = db.query(FraudLog).filter(FraudLog.risk_level == "Critical").count()
    high_count = db.query(FraudLog).filter(FraudLog.risk_level == "High").count()
    medium_count = db.query(FraudLog).filter(FraudLog.risk_level == "Medium").count()
    low_count = db.query(FraudLog).filter(FraudLog.risk_level == "Low").count()
    blacklisted_count = db.query(Blacklist).count()
    
    # Get last 10 fraud logs
    recent_logs = db.query(FraudLog).order_by(FraudLog.timestamp.desc()).limit(10).all()
    
    # Format recent logs
    formatted_logs = [
        {
            "phone_number": log.phone_number,
            "risk_score": log.risk_score,
            "risk_level": log.risk_level,
            "threat_category": log.threat_category,
            "confidence": log.confidence,
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for log in recent_logs
    ]
    
    # Get all blacklisted numbers
    blacklist = db.query(Blacklist).order_by(Blacklist.added_at.desc()).all()
    
    # Format blacklist
    formatted_blacklist = [
        {
            "phone_number": entry.phone_number,
            "reason": entry.reason,
            "added_at": entry.added_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for entry in blacklist
    ]
    
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "total_requests": total_requests,
        "critical_count": critical_count,
        "high_count": high_count,
        "medium_count": medium_count,
        "low_count": low_count,
        "blacklisted_count": blacklisted_count,
        "recent_logs": formatted_logs,
        "blacklist": formatted_blacklist
    })

@app.get("/history/{phone_number}")
async def get_history(
    phone_number: str, 
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_admin_key)
):
    """Get fraud analysis history for a phone number from database - Admin only."""
    logs = db.query(FraudLog).filter(FraudLog.phone_number == phone_number).order_by(FraudLog.timestamp.desc()).all()
    
    if not logs:
        return {
            "phone_number": phone_number,
            "history": [],
            "message": "No history found for this phone number"
        }
    
    history = [
        {
            "id": log.id,
            "phone_number": log.phone_number,
            "risk_score": log.risk_score,
            "risk_level": log.risk_level,
            "threat_category": log.threat_category,
            "confidence": log.confidence,
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for log in logs
    ]
    
    return {
        "phone_number": phone_number,
        "total_analyses": len(history),
        "history": history
    }

@app.get("/stats")
async def get_stats(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_admin_key)
):
    """Get fraud detection statistics - Admin only."""
    total_requests = db.query(FraudLog).count()
    critical_count = db.query(FraudLog).filter(FraudLog.risk_level == "Critical").count()
    high_count = db.query(FraudLog).filter(FraudLog.risk_level == "High").count()
    medium_count = db.query(FraudLog).filter(FraudLog.risk_level == "Medium").count()
    low_count = db.query(FraudLog).filter(FraudLog.risk_level == "Low").count()
    blacklisted_count = db.query(Blacklist).count()
    
    return {
        "total_requests": total_requests,
        "critical_count": critical_count,
        "high_count": high_count,
        "medium_count": medium_count,
        "low_count": low_count,
        "blacklisted_count": blacklisted_count
    }

@app.get("/config")
async def get_config(api_key: str = Depends(verify_admin_key)):
    """Get configuration summary - Admin only (no sensitive data)."""
    return {
        "status": "Configuration loaded successfully",
        "config": config.get_config_summary()
    }

@app.get("/blacklist")
async def get_blacklist(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_admin_key)
):
    """Get all blacklisted phone numbers - Admin only."""
    blacklisted = db.query(Blacklist).order_by(Blacklist.added_at.desc()).all()
    
    result = [
        {
            "id": entry.id,
            "phone_number": entry.phone_number,
            "reason": entry.reason,
            "added_at": entry.added_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for entry in blacklisted
    ]
    
    return {
        "total_blacklisted": len(result),
        "blacklist": result
    }

@app.websocket("/ws/dashboard")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for live dashboard updates."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def broadcast_update(db: Session):
    """Broadcast updated stats to all connected WebSocket clients."""
    # Get updated stats
    total_requests = db.query(FraudLog).count()
    critical_count = db.query(FraudLog).filter(FraudLog.risk_level == "Critical").count()
    high_count = db.query(FraudLog).filter(FraudLog.risk_level == "High").count()
    blacklisted_count = db.query(Blacklist).count()
    
    # Get latest log entry
    latest_log = db.query(FraudLog).order_by(FraudLog.timestamp.desc()).first()
    
    latest_entry = None
    if latest_log:
        latest_entry = {
            "phone_number": latest_log.phone_number or "N/A",
            "risk_score": latest_log.risk_score,
            "risk_level": latest_log.risk_level,
            "threat_category": latest_log.threat_category,
            "confidence": latest_log.confidence,
            "timestamp": latest_log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # Broadcast to all connected clients
    await manager.broadcast({
        "type": "update",
        "stats": {
            "total_requests": total_requests,
            "critical_count": critical_count,
            "high_count": high_count,
            "blacklisted_count": blacklisted_count
        },
        "latest_entry": latest_entry
    })

@app.post("/retrain")
async def retrain_model(
    training_data: dict,
    api_key: str = Depends(verify_admin_key)
):
    """Retrain the ML model with new data - Admin only."""
    scam_messages = training_data.get("scam_messages", [])
    legitimate_messages = training_data.get("legitimate_messages", [])
    
    if not scam_messages or not legitimate_messages:
        return {
            "status": "error",
            "message": "Both scam_messages and legitimate_messages are required"
        }
    
    # Retrain the model
    ml_model.retrain(scam_messages, legitimate_messages)
    
    total_samples = len(scam_messages) + len(legitimate_messages)
    
    return {
        "status": "Model retrained successfully",
        "new_training_samples": total_samples,
        "scam_samples": len(scam_messages),
        "legitimate_samples": len(legitimate_messages)
    }

