# Task API

A simple CRUD API built with FastAPI for managing a to-do list.

The API allows users to create, read, update, and delete tasks. Tasks are stored in memory, so the data resets whenever the server restarts.

## Features

* Create a new task
* View all tasks
* View a task by ID
* Update a task
* Mark a task as done
* Delete a task
* Health check endpoint
* Interactive Swagger UI documentation

## Installation and Running

Clone the repository and open the project folder.

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Run the API:

```powershell
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

## Endpoints

| Method | Endpoint      | Description                 |
| ------ | ------------- | --------------------------- |
| GET    | `/`           | Show API information        |
| GET    | `/health`     | Check if the API is running |
| GET    | `/tasks`      | Get all tasks               |
| GET    | `/tasks/{id}` | Get a task by ID            |
| POST   | `/tasks`      | Create a new task           |
| PUT    | `/tasks/{id}` | Update a task               |
| DELETE | `/tasks/{id}` | Delete a task               |

## Example Request

Create a new task:

```powershell
curl.exe -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"
```

Example response:

```text
HTTP/1.1 201 Created
date: [date]
server: uvicorn
content-length: [length]
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

FastAPI automatically generates interactive API documentation using Swagger UI.

Open:

```text
http://localhost:8000/docs
```

You can test all CRUD operations directly from the Swagger interface.

![alt text](image.png)

## Notes

Tasks are stored in an in-memory Python list rather than a database. This means any tasks created, updated, or deleted while the API is running will reset when the server restarts.
