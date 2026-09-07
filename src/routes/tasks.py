from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from models import NewTask, UpdateTask
from src.dependencies import service

router = APIRouter()

# show all tasks
@router.get("/tasks",summary="List all tasks")
def get_all_tasks():
    return service.get_all_tasks()

# show task by id
@router.get("/tasks/{id}",summary="Get a task by ID")
def get_one_task(id:int):

    task = service.get_task(id)

    if task is None:
          return JSONResponse(
                  status_code=404,
                  content={"error": "Task not found"}
              )
          
    return task

# create new task
@router.post("/tasks",summary="Create a new task")
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
@router.put("/tasks/{id}",summary="Update a task")
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
@router.delete("/tasks/{id}",summary="Delete a task")
def delete_task(id: int):

    deleted = service.delete_task(id)

    if not deleted:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return Response(status_code=204)