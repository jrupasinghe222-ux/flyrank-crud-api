import os
from dotenv import load_dotenv
from repository import SQLiteRepository
from service import TaskService
from supabase import create_client


load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

database_path = os.getenv("DATABASE_PATH", "tasks.db")

repository = SQLiteRepository(database_path)
repository.initialize_db()

service = TaskService(repository)

supabase = create_client(supabase_url,supabase_key)