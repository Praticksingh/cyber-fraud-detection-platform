"""
Test script to verify configuration system.
Tests environment variable loading and fallback defaults.
"""

import os
import sys


def test_config_defaults():
    """Test that config loads with default values (and no defaults for secret keys)."""
    print("\n" + "="*60)
    print("Testing Configuration - Default Values")
    print("="*60)
    
    # Clear any existing environment variables
    env_vars = [
        "PUBLIC_API_KEY", "ADMIN_API_KEY", "JWT_SECRET_KEY",
        "ALERT_EMAIL_ENABLED", "SMTP_HOST", "SMTP_PORT", "DATABASE_URL"
    ]
    
    for var in env_vars:
        if var in os.environ:
            del os.environ[var]
    
    # Re-import config to pick up the cleared environment
    if 'config' in sys.modules:
        del sys.modules['config']
    
    from config import config
    
    print(f"✓ PUBLIC_API_KEY: {'(set)' if config.PUBLIC_API_KEY else '(not set)'}  — required env var")
    print(f"✓ ADMIN_API_KEY: {'(set)' if config.ADMIN_API_KEY else '(not set)'}  — required env var")
    print(f"✓ JWT_SECRET_KEY: {'(set)' if config.JWT_SECRET_KEY else '(not set)'}  — required env var")
    print(f"✓ ALERT_EMAIL_ENABLED: {config.ALERT_EMAIL_ENABLED}")
    print(f"✓ SMTP_HOST: {config.SMTP_HOST}")
    print(f"✓ SMTP_PORT: {config.SMTP_PORT}")
    print(f"✓ DATABASE_URL: {config.DATABASE_URL}")
    
    # API keys and JWT secret have no built-in defaults — they must be supplied via env vars
    assert config.PUBLIC_API_KEY is None, "PUBLIC_API_KEY should be None when env var is not set"
    assert config.ADMIN_API_KEY is None, "ADMIN_API_KEY should be None when env var is not set"
    assert config.JWT_SECRET_KEY is None, "JWT_SECRET_KEY should be None when env var is not set"
    assert config.ALERT_EMAIL_ENABLED == False, "Default ALERT_EMAIL_ENABLED incorrect"
    assert config.SMTP_HOST == "smtp.gmail.com", "Default SMTP_HOST incorrect"
    assert config.SMTP_PORT == 587, "Default SMTP_PORT incorrect"
    
    print("\n✅ Default values loaded correctly (secret keys require env vars)!")
    return True


def test_config_environment():
    """Test that config loads from environment variables."""
    print("\n" + "="*60)
    print("Testing Configuration - Environment Variables")
    print("="*60)
    
    # Set environment variables
    os.environ["PUBLIC_API_KEY"] = "test-public-key"
    os.environ["ADMIN_API_KEY"] = "test-admin-key"
    os.environ["JWT_SECRET_KEY"] = "test-jwt-secret"
    os.environ["ALERT_EMAIL_ENABLED"] = "true"
    os.environ["SMTP_HOST"] = "smtp.test.com"
    os.environ["SMTP_PORT"] = "465"
    os.environ["DATABASE_URL"] = "sqlite:///test.db"
    
    # Reload config module
    if 'config' in sys.modules:
        del sys.modules['config']
    
    from config import config
    
    print(f"✓ PUBLIC_API_KEY: {config.PUBLIC_API_KEY}")
    print(f"✓ ADMIN_API_KEY: {config.ADMIN_API_KEY}")
    print(f"✓ JWT_SECRET_KEY: {'*' * len(config.JWT_SECRET_KEY)}")
    print(f"✓ ALERT_EMAIL_ENABLED: {config.ALERT_EMAIL_ENABLED}")
    print(f"✓ SMTP_HOST: {config.SMTP_HOST}")
    print(f"✓ SMTP_PORT: {config.SMTP_PORT}")
    print(f"✓ DATABASE_URL: {config.DATABASE_URL}")
    
    assert config.PUBLIC_API_KEY == "test-public-key", "Environment PUBLIC_API_KEY not loaded"
    assert config.ADMIN_API_KEY == "test-admin-key", "Environment ADMIN_API_KEY not loaded"
    assert config.JWT_SECRET_KEY == "test-jwt-secret", "Environment JWT_SECRET_KEY not loaded"
    assert config.ALERT_EMAIL_ENABLED == True, "Environment ALERT_EMAIL_ENABLED not loaded"
    assert config.SMTP_HOST == "smtp.test.com", "Environment SMTP_HOST not loaded"
    assert config.SMTP_PORT == 465, "Environment SMTP_PORT not loaded"
    assert config.DATABASE_URL == "sqlite:///test.db", "Environment DATABASE_URL not loaded"
    
    print("\n✅ All environment variables loaded correctly!")
    return True


def test_config_summary():
    """Test configuration summary (no sensitive data)."""
    print("\n" + "="*60)
    print("Testing Configuration Summary")
    print("="*60)
    
    # Reload with test environment
    if 'config' in sys.modules:
        del sys.modules['config']
    
    os.environ["SMTP_PASSWORD"] = "super-secret-password"
    os.environ["DATABASE_URL"] = "postgresql://user:password@localhost/fraud"
    
    from config import config
    
    summary = config.get_config_summary()
    
    print("Configuration Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Verify sensitive data is hidden
    assert "password" not in str(summary).lower(), "Password exposed in summary!"
    assert "***" in summary["database_url"], "Database path not hidden!"
    
    print("\n✅ Configuration summary is safe (no sensitive data)!")
    return True


def test_security_integration():
    """Test that security module uses config correctly."""
    print("\n" + "="*60)
    print("Testing Security Integration")
    print("="*60)
    
    # Set custom keys
    os.environ["PUBLIC_API_KEY"] = "custom-public"
    os.environ["ADMIN_API_KEY"] = "custom-admin"
    
    # Reload modules
    for module in ['config', 'security']:
        if module in sys.modules:
            del sys.modules[module]
    
    from security import verify_api_key
    from fastapi import Request
    
    # Create mock request with custom public key
    class MockRequest:
        def __init__(self, api_key):
            self.headers = {"X-API-KEY": api_key}
    
    # Test public key
    try:
        request = MockRequest("custom-public")
        result = verify_api_key(request)
        assert result == "public", "Public key verification failed"
        print("✓ Public key verification works")
    except Exception as e:
        print(f"✗ Public key verification failed: {e}")
        return False
    
    # Test admin key
    try:
        request = MockRequest("custom-admin")
        result = verify_api_key(request)
        assert result == "admin", "Admin key verification failed"
        print("✓ Admin key verification works")
    except Exception as e:
        print(f"✗ Admin key verification failed: {e}")
        return False
    
    print("\n✅ Security integration working correctly!")
    return True


def test_alert_service_integration():
    """Test that alert service uses config correctly."""
    print("\n" + "="*60)
    print("Testing Alert Service Integration")
    print("="*60)
    
    # Set alert configuration
    os.environ["ALERT_EMAIL_ENABLED"] = "true"
    os.environ["SMTP_HOST"] = "smtp.custom.com"
    os.environ["SMTP_PORT"] = "2525"
    os.environ["SMTP_USER"] = "test@example.com"
    os.environ["ALERT_WEBHOOK_URL"] = "https://webhook.test.com"
    
    # Reload modules
    for module in ['config', 'alert_service']:
        if module in sys.modules:
            del sys.modules[module]
    
    from alert_service import AlertService
    
    service = AlertService()
    
    assert service.email_enabled == True, "Email enabled not loaded"
    assert service.smtp_host == "smtp.custom.com", "SMTP host not loaded"
    assert service.smtp_port == 2525, "SMTP port not loaded"
    assert service.smtp_user == "test@example.com", "SMTP user not loaded"
    assert service.webhook_url == "https://webhook.test.com", "Webhook URL not loaded"
    
    print("✓ Email enabled:", service.email_enabled)
    print("✓ SMTP host:", service.smtp_host)
    print("✓ SMTP port:", service.smtp_port)
    print("✓ SMTP user:", service.smtp_user)
    print("✓ Webhook URL:", service.webhook_url)
    
    print("\n✅ Alert service integration working correctly!")
    return True


def main():
    """Run all configuration tests."""
    print("\n" + "="*60)
    print("CONFIGURATION SYSTEM TEST SUITE")
    print("="*60)
    
    results = {}
    
    try:
        results['defaults'] = test_config_defaults()
        results['environment'] = test_config_environment()
        results['summary'] = test_config_summary()
        results['security'] = test_security_integration()
        results['alerts'] = test_alert_service_integration()
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        for test_name, passed in results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{test_name.upper()}: {status}")
        
        total = len(results)
        passed = sum(results.values())
        print(f"\nTotal: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All configuration tests passed!")
            print("✅ System is ready for environment-based configuration!")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
