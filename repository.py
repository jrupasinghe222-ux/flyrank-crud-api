import sqlite3

class SQLiteRepository:
    def __init__(self,database_path):
        self.database_path = database_path

    def get_connection(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize_db(self):
        connection = self.get_connection()

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

    def get_all(self):

        connection = self.get_connection()
        tasks = connection.execute("SELECT * FROM tasks").fetchall()
        connection.close()

        return [dict(task) for task in tasks]

    def get_by_id(self,id):

        connection = self.get_connection()
        
        task = connection.execute("SELECT * FROM tasks WHERE id=?",
                               (id,)
                ).fetchone()
        
        connection.close()
        
        if task is None:
            return None

        return dict(task)

    def create_new(self,title):
        connection = self.get_connection()

        cursor = connection.execute(
                "INSERT INTO tasks(title,done) VALUES(?,?)",
                (title,False)
                )
        
        new_id = cursor.lastrowid
        
        new_task = {
            "id": new_id,
            "title": title,
            "done": False
         }
        
        connection.commit()
        connection.close()

        return new_task

    def update(self,id,title=None,done=None):
        connection = self.get_connection()

        if title is not None:
            connection.execute(
                    "UPDATE tasks SET title=? WHERE id=?",
                    (title,id)
                )

        if done is not None:
            connection.execute(
                    "UPDATE tasks SET done=? WHERE id=?",
                    (done,id)
                )

        connection.commit

        updated_task = connection.execute(
                "SELECT * FROM tasks WHERE id=?",
                (id,)
            ).fetchone()
        
        connection.close

        if updated_task is None:
            return None

        return dict(updated_task)

    def delete(self, task_id):
        connection = self.get_connection()

        cursor = connection.execute(
            "DELETE FROM tasks WHERE id=?",
            (task_id,)
        )

        connection.commit()
        connection.close()

        return cursor.rowcount > 0


                        

        

    