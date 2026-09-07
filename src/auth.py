from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase_auth.errors import AuthApiError
from src.dependencies import supabase

security = HTTPBearer(auto_error=False)

def get_current_user(credentials:HTTPAuthorizationCredentials | None = Depends(security)):

    if credentials is None or not credentials.credentials.strip():
        raise HTTPException(status_code=401, detail="Access token required")
    
    token = credentials.credentials
    
    try:
        supabase_response = supabase.auth.get_user(token)
    except AuthApiError:
        raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

    user = supabase_response.user

    return user
