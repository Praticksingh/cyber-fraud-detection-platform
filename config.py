"""
Configuration module for Cyber Fraud Detection System.
Loads settings from environment variables with fallback defaults for local development.
"""

import os


class Config:
    """Application configuration loaded from environment variables."""
    
    # API Keys — must be set via environment variables; no defaults are provided.
    PUBLIC_API_KEY = os.getenv("PUBLIC_API_KEY")
    ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")

    # JWT Secret — must be set via environment variable.
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    @classmethod
    def validate_required(cls) -> None:
        """Raise RuntimeError if any required environment variables are missing."""
        required = ("PUBLIC_API_KEY", "ADMIN_API_KEY", "JWT_SECRET_KEY")
        missing = [name for name in required if not getattr(cls, name)]
        if missing:
            raise RuntimeError(
                f"Missing required environment variable(s): {', '.join(missing)}. "
                "Please set them before starting the server."
            )
    
    # Alert Settings - Email
    ALERT_EMAIL_ENABLED = os.getenv("ALERT_EMAIL_ENABLED", "false").lower() == "true"
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO", "admin@example.com")
    
    # Alert Settings - Webhook
    ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL", "")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///fraud.db")
    
    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production mode."""
        return os.getenv("ENVIRONMENT", "development").lower() == "production"
    
    @classmethod
    def get_config_summary(cls) -> dict:
        """Get configuration summary (without sensitive data)."""
        return {
            "environment": os.getenv("ENVIRONMENT", "development"),
            "alert_email_enabled": cls.ALERT_EMAIL_ENABLED,
            "alert_webhook_enabled": bool(cls.ALERT_WEBHOOK_URL),
            "smtp_host": cls.SMTP_HOST,
            "smtp_port": cls.SMTP_PORT,
            "database_url": cls.DATABASE_URL.split("///")[0] + "///" + "***",  # Hide path
            "host": cls.HOST,
            "port": cls.PORT
        }


# Create a singleton instance
config = Config()
