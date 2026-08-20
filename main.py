from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from models import UpdateTask, NewTask
from repository import SQLiteRepository
from service import TaskService
from supabase import create_client
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

database_path = os.getenv("DATABASE_PATH", "tasks.db")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY") 

repository = SQLiteRepository(database_path)

repository.initialize_db()

service = TaskService(repository)

supabase = create_client(supabase_url,supabase_key)

print("Server running and connected to Supabase")


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