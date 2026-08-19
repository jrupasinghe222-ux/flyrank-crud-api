# Task API

A simple CRUD API built with FastAPI and SQLite for managing a to-do list.

The API allows users to create, read, update, and delete tasks. The application uses a service and repository architecture to separate the API logic from the database logic. The application is containerized with Docker and can be started using Docker Compose.

SQLite is used as the database, with the database file stored in a Docker volume so that task data persists even when the application container is stopped, removed, and recreated.

## Features

* Create a new task
* View all tasks
* View a task by ID
* Update a task
* Mark a task as done
* Delete a task
* Store tasks persistently using SQLite
* Repository and service architecture
* Environment-based database configuration
* Dockerized FastAPI application
* Docker Compose setup
* Persistent Docker volume for the database
* Health check endpoint
* Interactive Swagger UI documentation

## Architecture

The application is separated into three main layers:

```text
FastAPI Routes
      ↓
Task Service
      ↓
SQLite Repository
      ↓
SQLite Database
```

`main.py` contains the FastAPI routes and handles HTTP requests and responses.

`service.py` contains the application logic and validation.

`repository.py` contains the database operations and SQL queries.

The SQLite repository implements the storage operations used by the service. This means the routes do not directly access SQLite or execute SQL queries.

SQLite was used as the approved alternative to PostgreSQL for this project. The storage implementation was moved into the SQLite repository while the service and routes continue to interact with the repository through the same methods. Database-specific logic is therefore kept out of the service and route layers.

## Why SQLite?

SQLite was chosen because it is lightweight, simple to use, and does not require a separate database server. It stores the database in a single file while still allowing the project to demonstrate persistent storage, SQL operations, repository architecture, Docker volumes, and environment-based configuration.

## Database

The database contains a `tasks` table with the following columns:

| Column  | Type    | Description                                 |
| ------- | ------- | ------------------------------------------- |
| `id`    | INTEGER | Unique ID for each task and the primary key |
| `title` | TEXT    | The task title                              |
| `done`  | BOOLEAN | Whether the task has been completed         |

If the table is empty when the application starts, three example tasks are automatically added.

## Environment Configuration

The database path is configured using an environment variable

An `.env.example` file is included in the repository to show the required configuration:

## Running with Docker

### Requirements

Install Docker Desktop and make sure Docker is running.

Clone the repository and open the project directory.

Create your local `.env` file using `.env.example` as the template:

Build and start the application with:

```powershell
docker compose up --build
```

After the image has already been built, the stack can also be started with:

```powershell
docker compose up
```

The API will be available at:

```text
http://localhost:8000
```

Swagger UI is available at:

```text
http://localhost:8000/docs
```

To stop and remove the application container:

```powershell
docker compose down
```

The SQLite database remains stored in the Docker volume.

## Docker Persistence

SQLite data is stored in a Docker named volume mounted at `/data` inside the application container.

The persistence setup is:

```text
FastAPI Container
       ↓
/data/tasks.db
       ↓
Docker Named Volume
```

I verified persistence using the following process:

1. Started the application using Docker Compose.
2. Created a new task through the API.
3. Used `GET /tasks` to confirm that the task had been stored.
4. Ran:

   ```powershell
   docker compose down
   ```

   This stopped and removed the application container.

5. Started the application again using:

   ```powershell
   docker compose up -d
   ```

6. Used `GET /tasks` again and confirmed that the previously created task was still present.

This proves that the task data survives both application restarts and container removal/recreation because `tasks.db` is stored in the persistent Docker volume rather than inside the container's temporary filesystem.

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

## Example SQL Query

The database can also be queried directly using SQLite. For example, this query returns all completed tasks:

```sql
SELECT * FROM tasks WHERE done = 1;
```

Other SQL operations were used to inspect, update, and delete task records directly from the database.

## Database Viewer

The SQLite database was opened using DB Browser for SQLite to inspect the `tasks` table and execute SQL queries manually.

![Database Viewer](database.png)

## Swagger UI

FastAPI automatically generates interactive API documentation using Swagger UI.

Open:

```text
http://localhost:8000/docs
```

The full CRUD API can be tested directly through the Swagger interface.

![Swagger UI](image.png)