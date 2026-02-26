# Bcrypt Compatibility Fix

## Issue
Login and registration were failing with the error:
```
ValueError: password cannot be longer than 72 bytes, truncate manually if necessary
AttributeError: module 'bcrypt' has no attribute '__about__'
```

## Root Cause
The `passlib` library (version 1.7.4) has compatibility issues with:
- Python 3.14
- Newer versions of bcrypt (5.0.0+)

The issue occurred because passlib tries to access `bcrypt.__about__.__version__` which was removed in newer bcrypt versions. This caused the library to fail during initialization, even with short passwords.

## Solution
Replaced passlib with direct bcrypt usage:

### Changes Made

1. **auth.py**
   - Removed `passlib.context.CryptContext`
   - Imported `bcrypt` directly
   - Rewrote `get_password_hash()` to use `bcrypt.hashpw()` directly
   - Rewrote `verify_password()` to use `bcrypt.checkpw()` directly
   - Added proper error handling and byte conversion

2. **requirements.txt**
   - Removed: `passlib[bcrypt]==1.7.4`
   - Added: `bcrypt==4.1.2`

### New Implementation

```python
import bcrypt

def get_password_hash(password: str) -> str:
    """Hash a password with bcrypt."""
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must not exceed 72 characters"
        )
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    password_bytes = plain_password.encode('utf-8')
    hash_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hash_bytes)
```

## Testing Results

✅ Password hashing: Working
✅ Password verification: Working
✅ User registration: Working (Status 201)
✅ User login: Working (Status 200, JWT token returned)

## Installation

To apply the fix:

```bash
pip install bcrypt==4.1.2
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Compatibility

- Python 3.9+
- bcrypt 4.1.2
- Works with Python 3.14

## Security Notes

- Password validation still enforced (8-72 chars, uppercase, lowercase, number, special char)
- Bcrypt salt automatically generated for each password
- 72-byte limit properly enforced before hashing
- All existing security features maintained
