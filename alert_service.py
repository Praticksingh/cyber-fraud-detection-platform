import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from config import config


class AlertService:
    """Service for sending alerts via email and webhook."""
    
    def __init__(self):
        # Load configuration from config module
        self.email_enabled = config.ALERT_EMAIL_ENABLED
        self.smtp_host = config.SMTP_HOST
        self.smtp_port = config.SMTP_PORT
        self.smtp_user = config.SMTP_USER
        self.smtp_password = config.SMTP_PASSWORD
        self.alert_email_to = config.ALERT_EMAIL_TO
        self.webhook_url = config.ALERT_WEBHOOK_URL
    
    def send_alert(
        self,
        phone_number: str,
        risk_score: int,
        risk_level: str,
        threat_category: str,
        primary_reason: str
    ):
        """
        Send alert for critical fraud detection.
        
        Args:
            phone_number: The phone number flagged
            risk_score: Risk score (0-100)
            risk_level: Risk level (Critical/High/Medium/Low)
            threat_category: Category of threat
            primary_reason: Main reason for flagging
        """
        # Send email alert
        if self.email_enabled and self.smtp_user and self.smtp_password:
            try:
                self._send_email_alert(
                    phone_number, risk_score, risk_level, 
                    threat_category, primary_reason
                )
            except Exception as e:
                print(f"Email alert failed: {e}")
        
        # Send webhook alert
        if self.webhook_url:
            try:
                self._send_webhook_alert(
                    phone_number, risk_score, risk_level,
                    threat_category, primary_reason
                )
            except Exception as e:
                print(f"Webhook alert failed: {e}")
    
    def _send_email_alert(
        self,
        phone_number: str,
        risk_score: int,
        risk_level: str,
        threat_category: str,
        primary_reason: str
    ):
        """Send email alert using SMTP."""
        subject = f"🚨 CRITICAL FRAUD ALERT - {threat_category}"
        
        body = f"""
        CRITICAL FRAUD DETECTION ALERT
        
        A critical fraud threat has been detected:
        
        Phone Number: {phone_number}
        Risk Score: {risk_score}/100
        Risk Level: {risk_level}
        Threat Category: {threat_category}
        Reason: {primary_reason}
        
        This phone number has been automatically blacklisted.
        
        Please review immediately.
        
        ---
        Cyber Fraud Detection System
        """
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = self.alert_email_to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
        
        print(f"Email alert sent to {self.alert_email_to}")
    
    def _send_webhook_alert(
        self,
        phone_number: str,
        risk_score: int,
        risk_level: str,
        threat_category: str,
        primary_reason: str
    ):
        """Send webhook alert via HTTP POST."""
        payload = {
            "alert_type": "critical_fraud",
            "phone_number": phone_number,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "threat_category": threat_category,
            "primary_reason": primary_reason,
            "action": "automatically_blacklisted"
        }
        
        response = requests.post(
            self.webhook_url,
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"Webhook alert sent to {self.webhook_url}")
        else:
            print(f"Webhook alert failed: {response.status_code}")
