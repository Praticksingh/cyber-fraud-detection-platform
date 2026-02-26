"""
Platform startup script - Starts both backend and frontend servers.
Ensures proper initialization and connectivity.
"""
import subprocess
import sys
import time
import requests
import os
from pathlib import Path


def check_port(port):
    """Check if a port is in use."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0


def wait_for_backend(max_attempts=30):
    """Wait for backend to be ready."""
    print("Waiting for backend to start...")
    for i in range(max_attempts):
        try:
            response = requests.get('http://localhost:8000/', timeout=2)
            if response.status_code == 200:
                print("✓ Backend is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
        print(f"  Attempt {i+1}/{max_attempts}...")
    return False


def start_backend():
    """Start the FastAPI backend server."""
    print("\n" + "="*80)
    print("Starting Backend Server (FastAPI)")
    print("="*80)
    
    if check_port(8000):
        print("✓ Backend already running on port 8000")
        return None
    
    try:
        # Start backend in a new process
        if sys.platform == 'win32':
            backend_process = subprocess.Popen(
                ['python', '-m', 'uvicorn', 'main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            backend_process = subprocess.Popen(
                ['python', '-m', 'uvicorn', 'main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        
        # Wait for backend to be ready
        if wait_for_backend():
            print("✓ Backend started successfully on http://localhost:8000")
            return backend_process
        else:
            print("✗ Backend failed to start within timeout")
            return None
            
    except Exception as e:
        print(f"✗ Error starting backend: {str(e)}")
        return None


def start_frontend():
    """Start the React frontend server."""
    print("\n" + "="*80)
    print("Starting Frontend Server (React)")
    print("="*80)
    
    if check_port(3000):
        print("✓ Frontend already running on port 3000")
        return None
    
    try:
        frontend_dir = Path('frontend')
        if not frontend_dir.exists():
            print("✗ Frontend directory not found")
            return None
        
        # Check if node_modules exists
        if not (frontend_dir / 'node_modules').exists():
            print("Installing frontend dependencies...")
            subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
        
        # Start frontend in a new process
        if sys.platform == 'win32':
            frontend_process = subprocess.Popen(
                ['npm', 'start'],
                cwd=frontend_dir,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            frontend_process = subprocess.Popen(
                ['npm', 'start'],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        
        print("✓ Frontend starting on http://localhost:3000")
        print("  (This may take a minute...)")
        return frontend_process
        
    except Exception as e:
        print(f"✗ Error starting frontend: {str(e)}")
        return None


def test_connectivity():
    """Test connectivity between frontend and backend."""
    print("\n" + "="*80)
    print("Testing Connectivity")
    print("="*80)
    
    # Test backend
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            print("✓ Backend API is accessible")
            data = response.json()
            print(f"  Version: {data.get('version', 'unknown')}")
        else:
            print(f"✗ Backend returned status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Cannot connect to backend: {str(e)}")
    
    # Test registration endpoint
    try:
        test_data = {
            "username": "connectivity_test",
            "email": "test@connectivity.com",
            "password": "Test@1234"
        }
        response = requests.post('http://localhost:8000/register', json=test_data, timeout=5)
        if response.status_code in [201, 400]:  # 201 = success, 400 = already exists
            print("✓ Registration endpoint is working")
        else:
            print(f"⚠ Registration endpoint returned: {response.status_code}")
    except Exception as e:
        print(f"✗ Registration endpoint error: {str(e)}")
    
    print("\n" + "="*80)
    print("Platform Status")
    print("="*80)
    print(f"Backend:  http://localhost:8000")
    print(f"Frontend: http://localhost:3000")
    print(f"API Docs: http://localhost:8000/docs")
    print("="*80)


def main():
    """Main function to start the platform."""
    print("\n" + "="*80)
    print("Cyber Fraud Detection Platform - Startup Script")
    print("="*80)
    
    # Start backend
    backend_process = start_backend()
    
    # Start frontend
    frontend_process = start_frontend()
    
    # Test connectivity
    time.sleep(3)  # Give servers time to initialize
    test_connectivity()
    
    print("\n" + "="*80)
    print("Platform is running!")
    print("="*80)
    print("\nPress Ctrl+C to stop all servers")
    print("\nQuick Links:")
    print("  - Frontend: http://localhost:3000")
    print("  - Backend API: http://localhost:8000")
    print("  - API Documentation: http://localhost:8000/docs")
    print("  - Register: http://localhost:3000/register")
    print("  - Login: http://localhost:3000/login")
    
    try:
        # Keep script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✓ Platform stopped")


if __name__ == "__main__":
    main()
