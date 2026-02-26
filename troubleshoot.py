"""
Troubleshooting script for the Cyber Fraud Detection Platform.
Checks common issues and provides solutions.
"""
import requests
import socket
import sys
from pathlib import Path


def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*80)
    print(title)
    print("="*80)


def check_port(port, service_name):
    """Check if a port is in use."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    
    if result == 0:
        print(f"✓ {service_name} port {port} is OPEN (service is running)")
        return True
    else:
        print(f"✗ {service_name} port {port} is CLOSED (service is NOT running)")
        return False


def test_backend_api():
    """Test backend API connectivity."""
    print_header("Backend API Test")
    
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        print(f"✓ Backend is accessible")
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Message: {data.get('message', 'N/A')}")
            print(f"  Version: {data.get('version', 'N/A')}")
            return True
        return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend")
        print("  Solution: Start the backend with: python -m uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_registration_endpoint():
    """Test registration endpoint."""
    print_header("Registration Endpoint Test")
    
    try:
        test_data = {
            "username": "test_user_" + str(int(time.time())),
            "email": f"test_{int(time.time())}@example.com",
            "password": "Test@1234"
        }
        
        response = requests.post(
            'http://localhost:8000/register',
            json=test_data,
            timeout=5
        )
        
        print(f"✓ Registration endpoint is accessible")
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print(f"  Response: {response.json()}")
            print("✓ Registration is working correctly!")
            return True
        elif response.status_code == 400:
            print(f"  Response: {response.json()}")
            print("✓ Endpoint is working (user already exists)")
            return True
        else:
            print(f"  Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to registration endpoint")
        print("  Solution: Ensure backend is running on port 8000")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def check_cors():
    """Check CORS configuration."""
    print_header("CORS Configuration Check")
    
    try:
        response = requests.options(
            'http://localhost:8000/register',
            headers={
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            },
            timeout=5
        )
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        
        print("✓ CORS headers present:")
        for header, value in cors_headers.items():
            if value:
                print(f"  {header}: {value}")
        
        if cors_headers['Access-Control-Allow-Origin']:
            print("✓ CORS is properly configured")
            return True
        else:
            print("✗ CORS might not be configured correctly")
            return False
            
    except Exception as e:
        print(f"⚠ Could not check CORS: {str(e)}")
        return False


def check_frontend_files():
    """Check if frontend files exist."""
    print_header("Frontend Files Check")
    
    frontend_dir = Path('frontend')
    
    checks = [
        ('Frontend directory', frontend_dir),
        ('package.json', frontend_dir / 'package.json'),
        ('src directory', frontend_dir / 'src'),
        ('Register.js', frontend_dir / 'src' / 'pages' / 'Register.js'),
        ('node_modules', frontend_dir / 'node_modules'),
        ('.env.development', frontend_dir / '.env.development'),
    ]
    
    all_good = True
    for name, path in checks:
        if path.exists():
            print(f"✓ {name} exists")
        else:
            print(f"✗ {name} is missing")
            all_good = False
            
            if name == 'node_modules':
                print("  Solution: Run 'npm install' in the frontend directory")
            elif name == '.env.development':
                print("  Solution: Create .env.development with REACT_APP_API_URL=http://localhost:8000")
    
    return all_good


def check_environment_variables():
    """Check environment variables."""
    print_header("Environment Variables Check")
    
    env_file = Path('frontend/.env.development')
    if env_file.exists():
        print("✓ .env.development file exists")
        with open(env_file, 'r') as f:
            content = f.read()
            if 'REACT_APP_API_URL' in content:
                print("✓ REACT_APP_API_URL is defined")
                # Extract the URL
                for line in content.split('\n'):
                    if line.startswith('REACT_APP_API_URL'):
                        print(f"  Value: {line.split('=')[1].strip()}")
            else:
                print("✗ REACT_APP_API_URL is not defined")
                print("  Solution: Add REACT_APP_API_URL=http://localhost:8000 to .env.development")
    else:
        print("✗ .env.development file not found")
        print("  Solution: Create frontend/.env.development with:")
        print("    REACT_APP_API_URL=http://localhost:8000")


def check_database():
    """Check database connectivity."""
    print_header("Database Check")
    
    try:
        from database import SessionLocal
        from db_models import User
        
        db = SessionLocal()
        user_count = db.query(User).count()
        db.close()
        
        print(f"✓ Database is accessible")
        print(f"  Total users: {user_count}")
        return True
    except Exception as e:
        print(f"✗ Database error: {str(e)}")
        print("  Solution: Run 'python -c \"from database import init_db; init_db()\"'")
        return False


def provide_solutions():
    """Provide common solutions."""
    print_header("Common Solutions")
    
    print("\n1. Backend not running:")
    print("   python -m uvicorn main:app --reload")
    
    print("\n2. Frontend not running:")
    print("   cd frontend")
    print("   npm start")
    
    print("\n3. Network Error in frontend:")
    print("   - Check if backend is running on port 8000")
    print("   - Check .env.development has REACT_APP_API_URL=http://localhost:8000")
    print("   - Restart frontend after changing .env file")
    
    print("\n4. Registration fails:")
    print("   - Check backend logs for errors")
    print("   - Verify database is initialized")
    print("   - Check if email/username already exists")
    
    print("\n5. Start everything at once:")
    print("   python start_platform.py")


def main():
    """Main troubleshooting function."""
    import time
    
    print("\n" + "="*80)
    print("Cyber Fraud Detection Platform - Troubleshooting")
    print("="*80)
    
    # Check ports
    print_header("Port Status Check")
    backend_running = check_port(8000, "Backend")
    frontend_running = check_port(3000, "Frontend")
    
    # Check backend
    if backend_running:
        backend_ok = test_backend_api()
        if backend_ok:
            test_registration_endpoint()
            check_cors()
    else:
        print("\n⚠ Backend is not running. Start it with:")
        print("  python -m uvicorn main:app --reload")
    
    # Check frontend
    check_frontend_files()
    check_environment_variables()
    
    # Check database
    check_database()
    
    # Provide solutions
    provide_solutions()
    
    print("\n" + "="*80)
    print("Troubleshooting Complete")
    print("="*80)


if __name__ == "__main__":
    import time
    main()
