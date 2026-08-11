from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()

TASKS = [
    {
        "id":1,
        "title":"Get goceries",
        "done":False
    },
    {
        "id":2,
        "title":"Write email",
        "done":False
    },
    {
         "id":3,
        "title":"Water plants",
        "done":False
    }
]

class NewTask(BaseModel):
    title: str | None = None

class UpdateTask(BaseModel):
    title: str | None = None
    done: bool | None = None

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
    return TASKS

# show task by id
@app.get("/tasks/{id}",summary="Get a task by ID")
def get_one_task(id:int):

    for task in TASKS:
        if task["id"] == id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

# create new task
@app.post("/tasks",summary="Create a new task")
def create_task(task: NewTask):

    if task.title is None or task.title.strip() == "":
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )

    new_id = max(task["id"] for task in TASKS) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }

    TASKS.append(new_task)

    return JSONResponse(
        status_code=201,
        content=new_task
    )

# update task
@app.put("/tasks/{id}",summary="Update a task")
def update_task(id: int, updated_data: UpdateTask):

    for task in TASKS:
        if task["id"] == id:

            if updated_data.title is None and updated_data.done is None:
                return JSONResponse(
                    status_code=400,
                    content={"error": "No update data provided"}
                )

            if updated_data.title is not None and updated_data.title.strip() == "":
                return JSONResponse(
                    status_code=400,
                    content={"error": "Title cannot be empty"}
                )

            if updated_data.title is not None:
                task["title"] = updated_data.title

            if updated_data.done is not None:
                task["done"] = updated_data.done

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

# delete task
@app.delete("/tasks/{id}",summary="Delete a task")
def delete_task(id: int):

    for task in TASKS:
        if task["id"] == id:
            TASKS.remove(task)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )