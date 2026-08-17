from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import sqlite3

app = FastAPI()

def get_db_connection():
    connection = sqlite3.connect("tasks.db")
    connection.row_factory = sqlite3.Row
    return connection

def initialize_db():
    connection = get_db_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        done BOOLEAN
        )
        """
    )

    example_tasks = [
    ("Get groceries",False),
    ("Write email",False),
    ("Water plants",False)
    ]

    count = connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]

    if count == 0:
        connection.executemany("INSERT INTO tasks(title,done) VALUES (?,?)",
                        example_tasks
                    )

    connection.commit()
    connection.close()

initialize_db()

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

    connection = get_db_connection()
    tasks = connection.execute("SELECT * FROM tasks").fetchall()
    connection.close()

    return [dict(task) for task in tasks]

# show task by id
@app.get("/tasks/{id}",summary="Get a task by ID")
def get_one_task(id:int):

    connection = get_db_connection()

    task = connection.execute("SELECT * FROM tasks WHERE id=?",
                       (id,)
        ).fetchone()

    connection.close()

    if task is not None:
        return dict(task)

    return JSONResponse(
        status_code=404,
        content={"error: Task not found"}
    )

# create new task
@app.post("/tasks",summary="Create a new task")
def create_task(task: NewTask):

    if task.title is None or task.title.strip() == "":
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )

    connection = get_db_connection()

    cursor = connection.execute(
        "INSERT INTO tasks(title,done) VALUES(?,?)",
        (task.title,False)
        )

    new_id = cursor.lastrowid

    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }

    connection.commit()
    connection.close()

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