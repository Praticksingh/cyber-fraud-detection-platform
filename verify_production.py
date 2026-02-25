"""
Production Verification Script
Verifies the system is production-ready.
"""

import os
import sys
from pathlib import Path


def check_file_exists(filepath, required=True):
    """Check if a file exists."""
    exists = Path(filepath).exists()
    status = "✓" if exists else "✗"
    req = "(required)" if required else "(optional)"
    print(f"{status} {filepath} {req}")
    return exists if required else True


def check_no_hardcoded_secrets():
    """Check for hardcoded secrets in source files."""
    print("\n🔒 Checking for hardcoded secrets...")
    
    # Files to check
    files_to_check = [
        "security.py",
        "alert_service.py",
        "database.py",
        "main.py"
    ]
    
    suspicious_patterns = [
        "password = ",
        "api_key = ",
        "secret = ",
        "token = "
    ]
    
    issues = []
    for filepath in files_to_check:
        if not Path(filepath).exists():
            continue
            
        with open(filepath, 'r') as f:
            content = f.read().lower()
            for pattern in suspicious_patterns:
                if pattern in content and "config." not in content:
                    issues.append(f"{filepath}: Found '{pattern}'")
    
    if issues:
        print("✗ Found potential hardcoded secrets:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✓ No hardcoded secrets found")
        return True


def check_gitignore():
    """Check .gitignore has necessary entries."""
    print("\n📝 Checking .gitignore...")
    
    required_entries = [
        ".env",
        "fraud.db",
        "model.pkl",
        "__pycache__",
        "*.pyc",
        "*.log"
    ]
    
    if not Path(".gitignore").exists():
        print("✗ .gitignore not found")
        return False
    
    with open(".gitignore", 'r') as f:
        content = f.read()
    
    missing = []
    for entry in required_entries:
        if entry not in content:
            missing.append(entry)
    
    if missing:
        print("✗ Missing entries in .gitignore:")
        for entry in missing:
            print(f"  - {entry}")
        return False
    else:
        print("✓ .gitignore is complete")
        return True


def check_docker_files():
    """Check Docker files are present and valid."""
    print("\n🐳 Checking Docker files...")
    
    docker_ok = check_file_exists("Dockerfile")
    compose_ok = check_file_exists("docker-compose.yml")
    dockerignore_ok = check_file_exists(".dockerignore")
    
    # Check Dockerfile has non-root user
    if docker_ok:
        with open("Dockerfile", 'r') as f:
            content = f.read()
            if "USER appuser" in content or "USER " in content:
                print("✓ Dockerfile uses non-root user")
            else:
                print("⚠ Dockerfile should use non-root user")
    
    return docker_ok and compose_ok and dockerignore_ok


def check_configuration():
    """Check configuration setup."""
    print("\n⚙️  Checking configuration...")
    
    config_ok = check_file_exists("config.py")
    env_example_ok = check_file_exists(".env.example")
    
    # Check config.py uses os.getenv
    if config_ok:
        with open("config.py", 'r') as f:
            content = f.read()
            if "os.getenv" in content:
                print("✓ config.py uses environment variables")
            else:
                print("✗ config.py should use os.getenv")
                return False
    
    return config_ok and env_example_ok


def check_documentation():
    """Check documentation files."""
    print("\n📚 Checking documentation...")
    
    docs = [
        ("README.md", True),
        ("QUICKSTART.md", True),
        ("DEPLOYMENT.md", True),
        ("CONFIGURATION.md", True),
        ("PRODUCTION_CHECKLIST.md", True),
        (".env.example", True)
    ]
    
    all_ok = True
    for doc, required in docs:
        if not check_file_exists(doc, required):
            all_ok = False
    
    return all_ok


def check_requirements():
    """Check requirements.txt."""
    print("\n📦 Checking requirements.txt...")
    
    if not Path("requirements.txt").exists():
        print("✗ requirements.txt not found")
        return False
    
    with open("requirements.txt", 'r') as f:
        content = f.read()
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "scikit-learn",
        "jinja2"
    ]
    
    missing = []
    for package in required_packages:
        if package not in content.lower():
            missing.append(package)
    
    if missing:
        print("✗ Missing packages in requirements.txt:")
        for package in missing:
            print(f"  - {package}")
        return False
    else:
        print("✓ requirements.txt is complete")
        return True


def check_tests():
    """Check test files exist."""
    print("\n🧪 Checking test files...")
    
    test_files = [
        "test_api.py",
        "test_config.py",
        "test_advanced_features.py"
    ]
    
    all_ok = True
    for test_file in test_files:
        if not check_file_exists(test_file, required=False):
            all_ok = False
    
    return all_ok


def main():
    """Run all production verification checks."""
    print("="*60)
    print("PRODUCTION VERIFICATION")
    print("="*60)
    
    checks = {
        "Configuration": check_configuration(),
        "Docker Files": check_docker_files(),
        "Gitignore": check_gitignore(),
        "Requirements": check_requirements(),
        "Documentation": check_documentation(),
        "No Hardcoded Secrets": check_no_hardcoded_secrets(),
        "Tests": check_tests()
    }
    
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    for check_name, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name}: {status}")
    
    total = len(checks)
    passed = sum(checks.values())
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 System is PRODUCTION READY!")
        print("✅ All verification checks passed")
        print("\nNext steps:")
        print("1. Review PRODUCTION_CHECKLIST.md")
        print("2. Set production environment variables")
        print("3. Deploy to production")
        return 0
    else:
        print(f"\n⚠️  {total - passed} check(s) failed")
        print("Please fix the issues above before deploying to production")
        return 1


if __name__ == "__main__":
    sys.exit(main())
