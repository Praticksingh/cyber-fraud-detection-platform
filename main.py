from fastapi import FastAPI, Request, Depends, WebSocket, WebSocketDisconnect, BackgroundTasks, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
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
from datetime import datetime, timedelta
from database import get_db, init_db
from db_models import FraudLog, Blacklist, User
from security import verify_api_key, verify_admin_key
from alert_service import AlertService
from config import config
from graph_service import fraud_graph
from auth import (
    UserRegister, UserLogin, Token,
    authenticate_user, create_user, create_access_token,
    get_user_by_username, get_user_by_email,
    get_current_user, get_current_admin_user
)
from typing import List
import json
import os

app = FastAPI(title="Cyber Fraud Detection System")

# Configure CORS for frontend - Allow both local and production origins
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://cyber-fraud-detection-platform.vercel.app",
    "https://*.vercel.app",  # Allow all Vercel preview deployments
]

# Add custom frontend URL from environment if provided
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now (can be restricted later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

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


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user account with comprehensive password validation."""
    try:
        # Check if username already exists
        existing_user = get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        existing_email = get_user_by_email(db, user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user (password validation handled by Pydantic)
        user = create_user(
            db=db,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            role="user"  # Default role
        )
        
        return {
            "message": "User registered successfully",
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log and return generic error for unexpected issues
        print(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@app.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login with username or email and receive JWT token."""
    # Authenticate user (accepts username or email)
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        username=user.username
    )

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
    
    # Step 10: Add to knowledge graph
    if phone:
        # Add phone number to graph
        fraud_graph.add_entity("phone", phone, final_score)
        
        # If high risk, propagate risk to connected entities
        if final_score > 70:
            fraud_graph.propagate_risk(phone, decay_factor=0.7)
        
        # Create relationships based on patterns
        if detection_results.get("threat_matches"):
            for threat in detection_results["threat_matches"]:
                fraud_graph.add_relationship(phone, f"pattern:{threat}", "exhibits_pattern", 0.8)
    
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
    current_user: User = Depends(get_current_admin_user)
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

@app.get("/history")
async def get_all_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all fraud analysis history from database - Authenticated users."""
    logs = db.query(FraudLog).order_by(FraudLog.timestamp.desc()).all()
    
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
    
    return history


@app.get("/history/{phone_number}")
async def get_history(
    phone_number: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get fraud analysis history for a phone number from database - Authenticated users."""
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
    current_user: User = Depends(get_current_user)
):
    """Get fraud detection statistics - Authenticated users."""
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
async def get_config(current_user: User = Depends(get_current_admin_user)):
    """Get configuration summary - Admin only (no sensitive data)."""
    return {
        "status": "Configuration loaded successfully",
        "config": config.get_config_summary()
    }

@app.get("/blacklist")
async def get_blacklist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
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


@app.post("/blacklist", status_code=status.HTTP_201_CREATED)
async def add_to_blacklist(
    blacklist_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Add a phone number to blacklist - Admin only."""
    phone_number = blacklist_data.get("phone_number")
    reason = blacklist_data.get("reason")
    
    if not phone_number or not reason:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number and reason are required"
        )
    
    # Check if already blacklisted
    existing = db.query(Blacklist).filter(Blacklist.phone_number == phone_number).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already blacklisted"
        )
    
    # Add to blacklist
    blacklist_entry = Blacklist(
        phone_number=phone_number,
        reason=reason,
        added_at=datetime.now()
    )
    db.add(blacklist_entry)
    db.commit()
    db.refresh(blacklist_entry)
    
    return {
        "message": "Phone number added to blacklist",
        "id": blacklist_entry.id,
        "phone_number": blacklist_entry.phone_number
    }


@app.delete("/blacklist/{blacklist_id}")
async def remove_from_blacklist(
    blacklist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Remove a phone number from blacklist - Admin only."""
    blacklist_entry = db.query(Blacklist).filter(Blacklist.id == blacklist_id).first()
    
    if not blacklist_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blacklist entry not found"
        )
    
    phone_number = blacklist_entry.phone_number
    db.delete(blacklist_entry)
    db.commit()
    
    return {
        "message": "Phone number removed from blacklist",
        "phone_number": phone_number
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

async def retrain_model(
    training_data: dict,
    current_user: User = Depends(get_current_admin_user)
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


@app.get("/graph")
async def get_graph(limit: int = 100):
    """Get knowledge graph data for visualization - Public endpoint."""
    graph_data = fraud_graph.get_graph_data_for_visualization(limit=limit)
    graph_stats = fraud_graph.get_statistics()
    
    return {
        "nodes": graph_data["nodes"],
        "edges": graph_data["edges"],
        "statistics": graph_stats
    }

@app.get("/analytics/summary")
async def get_analytics_summary(db: Session = Depends(get_db)):
    """Get analytics summary - Public endpoint."""
    total_scans = db.query(FraudLog).count()
    high_risk = db.query(FraudLog).filter(
        FraudLog.risk_level.in_(["High", "Critical"])
    ).count()
    medium_risk = db.query(FraudLog).filter(FraudLog.risk_level == "Medium").count()
    low_risk = db.query(FraudLog).filter(FraudLog.risk_level == "Low").count()
    
    return {
        "total_scans": total_scans,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk
    }

@app.get("/analytics/distribution")
async def get_analytics_distribution(db: Session = Depends(get_db)):
    """Get risk level distribution - Public endpoint."""
    critical = db.query(FraudLog).filter(FraudLog.risk_level == "Critical").count()
    high = db.query(FraudLog).filter(FraudLog.risk_level == "High").count()
    medium = db.query(FraudLog).filter(FraudLog.risk_level == "Medium").count()
    low = db.query(FraudLog).filter(FraudLog.risk_level == "Low").count()
    
    return {
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low
    }

@app.get("/analytics/trends")
async def get_analytics_trends(days: int = 30, db: Session = Depends(get_db)):
    """Get fraud detection trends over time - Public endpoint."""
    # Get date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Query logs grouped by date
    logs = db.query(
        func.date(FraudLog.timestamp).label('date'),
        func.count(FraudLog.id).label('count')
    ).filter(
        FraudLog.timestamp >= start_date
    ).group_by(
        func.date(FraudLog.timestamp)
    ).order_by(
        func.date(FraudLog.timestamp)
    ).all()
    
    # Format results
    trends = [
        {
            "date": log.date.strftime("%Y-%m-%d") if hasattr(log.date, 'strftime') else str(log.date),
            "count": log.count
        }
        for log in logs
    ]
    
    # Fill in missing dates with zero counts
    date_map = {trend["date"]: trend["count"] for trend in trends}
    result = []
    
    for i in range(days):
        date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        result.append({
            "date": date,
            "count": date_map.get(date, 0)
        })
    
    return result


