from fastapi import FastAPI, Response, Header, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import UpdateTask, NewTask, AuthCredentials
from repository import SQLiteRepository
from service import TaskService
from supabase import create_client
import os
from dotenv import load_dotenv
from supabase_auth.errors import AuthApiError


app = FastAPI()

load_dotenv()

database_path = os.getenv("DATABASE_PATH", "tasks.db")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY") 

repository = SQLiteRepository(database_path)

repository.initialize_db()

service = TaskService(repository)

supabase = create_client(supabase_url,supabase_key)

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


@app.get("/",summary="Show API information")
def home():
    return { "name": "Task API", 
            "version": "1.0", 
            "endpoints": [
            "GET /tasks",
            "GET /tasks/{id}",
            "POST /tasks",
            "PUT /tasks/{id}",
            "DELETE /tasks/{id}",
            "GET /health"
            ]
        }

@app.get("/health",summary="Check API health")
def health_check():
    return { "status": "ok" }

# show all tasks
@app.get("/tasks",summary="List all tasks")
def get_all_tasks():
    return service.get_all_tasks()

# show task by id
@app.get("/tasks/{id}",summary="Get a task by ID")
def get_one_task(id:int):

    task = service.get_task(id)

    if task is None:
          return JSONResponse(
                  status_code=404,
                  content={"error": "Task not found"}
              )
          
    return task

    

# create new task
@app.post("/tasks",summary="Create a new task")
def create_task(task: NewTask):

    new_task = service.create_task(task.title)

    if new_task is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )
    
    return JSONResponse(
        status_code=201,
        content=new_task
    )

# update task
@app.put("/tasks/{id}",summary="Update a task")
def update_task(id: int, updated_data: UpdateTask):

    result = service.update_task(
        id,
        updated_data.title,
        updated_data.done
    )

    if result == "empty":
        return JSONResponse(
            status_code=400,
            content={"error": "No update data provided"}
        )

    if result == "invalid_title":
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )

    if result == "not_found":
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return result
    

# delete task
@app.delete("/tasks/{id}",summary="Delete a task")
def delete_task(id: int):

    deleted = service.delete_task(id)

    if not deleted:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return Response(status_code=204)

@app.post("/auth/signup",summary="Create a new account")
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
    except AuthApiError:
            return JSONResponse(
            status_code=400,
            content={"error": "Signup failed"}
            )

    return JSONResponse(
                status_code=201,
                content= supabase_response.user.model_dump(mode="json")
            )


@app.post("/auth/login",summary="Login to existing account")
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
            content={"error": "Invalid login credentials"}
            )

    return JSONResponse(
                status_code=200,
                content= {
                    "access_token": supabase_response.session.access_token,
                    "refresh_token": supabase_response.session.refresh_token
                }
            )


@app.get("/public/info")
def info():
    return JSONResponse(
            status_code=200,
            content={"message": "Welcome stranger! This info is public."}
        )

@app.get("/protected/profile")
def profile(user = Depends(get_current_user)):
    
    return JSONResponse(
                status_code=200,
                content= {
                    "id": user.id,
                    "email": user.email,
                    "created_at":str(user.created_at)
                }
    )

@app.get("/protected/dashboard")
def dashboard(user = Depends(get_current_user)):
    return JSONResponse(
                status_code=200,
                content={"message": "Welcome to your dashboard"}
            )

@app.post("/auth/logout")
def logout(user = Depends(get_current_user)):
    supabase.auth.sign_out()
    return Response(status_code=204)