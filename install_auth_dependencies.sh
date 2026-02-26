#!/bin/bash

# Install authentication dependencies for the backend
echo "Installing authentication dependencies..."

pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install python-multipart==0.0.6

echo "Authentication dependencies installed successfully!"
echo ""
echo "To start the backend with authentication:"
echo "uvicorn main:app --reload"
