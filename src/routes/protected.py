from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.auth import get_current_user

router = APIRouter()

@router.get("/protected/profile")
def profile(user = Depends(get_current_user)):
    
    return JSONResponse(
                status_code=200,
                content= {
                    "id": user.id,
                    "email": user.email,
                    "created_at":str(user.created_at)
                }
    )

@router.get("/protected/dashboard")
def dashboard(user = Depends(get_current_user)):
    return JSONResponse(
                status_code=200,
                content={"message": "Welcome to your dashboard"}
            )
