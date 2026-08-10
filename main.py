from fastapi import FastAPI
from fastapi.responses import JSONResponse

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

@app.get("/")
def home():
    return { "name": "Task API", 
            "version": "1.0", 
            "endpoints": ["/tasks"] 
            }

@app.get("/health")
def health_check():
    return { "status": "ok" }

@app.get("/tasks")
def get_all_tasks():
    return TASKS

@app.get("/tasks/{id}")
def get_one_task(id:int):

    for task in TASKS:
        if task["id"] == id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )