from fastapi import FastAPI
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

@app.get("/")
def home():
    return { "name": "Task API", 
            "version": "1.0", 
            "endpoints": ["/tasks"] 
            }

@app.get("/health")
def health_check():
    return { "status": "ok" }

# show all tasks
@app.get("/tasks")
def get_all_tasks():
    return TASKS

# show task by id
@app.get("/tasks/{id}")
def get_one_task(id:int):

    for task in TASKS:
        if task["id"] == id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

# create new task
@app.post("/tasks")
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
    