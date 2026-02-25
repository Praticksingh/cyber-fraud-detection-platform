from fastapi import Request, HTTPException, status
from config import config


def verify_api_key(request: Request) -> str:
    """
    Verify API key from request header.
    
    Args:
        request: FastAPI Request object
        
    Returns:
        API key type: "public" or "admin"
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    api_key = request.headers.get("X-API-KEY")
    
    # Check if API key is provided
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key"
        )
    
    # Validate API key
    if api_key == config.ADMIN_API_KEY:
        return "admin"
    elif api_key == config.PUBLIC_API_KEY:
        return "public"
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )


def verify_admin_key(request: Request) -> str:
    """
    Verify that the request has admin API key.
    
    Args:
        request: FastAPI Request object
        
    Returns:
        "admin" if valid admin key
        
    Raises:
        HTTPException: If not admin key
    """
    key_type = verify_api_key(request)
    
    if key_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return key_type
