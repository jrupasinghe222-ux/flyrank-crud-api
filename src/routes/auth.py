from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from supabase_auth.errors import AuthApiError
from models import AuthCredentials
from src.auth import get_current_user
from src.dependencies import supabase

router = APIRouter()

@router.post("/auth/signup",summary="Create a new account")
def signup(credentials:AuthCredentials):

    if credentials.email is None or credentials.password is None or credentials.password.strip() == "" or credentials.email.strip()=="":
        return JSONResponse(
            status_code=400,
            content={"error": "Email or Password cannot be empty"}
        )

    try:
        supabase_response = supabase.auth.sign_up(
                {
                    "email":credentials.email,
                    "password":credentials.password
                }
            )
    except AuthApiError as e:
            return JSONResponse(
            status_code=400,
            content={"error": f"Signup failed: {e}"}
            )

    return JSONResponse(
                status_code=201,
                content= supabase_response.user.model_dump(mode="json")
            )


@router.post("/auth/login",summary="Login to existing account")
def login(credentials:AuthCredentials):

    if credentials.email is None or credentials.password is None or credentials.password.strip() == "" or credentials.email.strip()=="":
        return JSONResponse(
            status_code=400,
            content={"error": "Email or Password cannot be empty"}
        )

    try:
        supabase_response = supabase.auth.sign_in_with_password(
                {
                    "email":credentials.email,
                    "password":credentials.password
                }
            )
    except AuthApiError as e:
            print(str(e))
            return JSONResponse(
            status_code=401,
            content={"error": f"Invalid login credentials"}
            )

    return JSONResponse(
                status_code=200,
                content= {
                    "access_token": supabase_response.session.access_token,
                    "refresh_token": supabase_response.session.refresh_token
                }
            )

@router.post("/auth/logout")
def logout(user = Depends(get_current_user)):
    supabase.auth.sign_out()
    return Response(status_code=204)