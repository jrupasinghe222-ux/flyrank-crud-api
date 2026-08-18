class TaskService:
    def __init__(self,repository):
        self.repository = repository

    def get_all_tasks(self):
        return self.repository.get_all()

    def get_task(self,task_id):
        return self.repository.get_by_id(task_id)

    def create_task(self,title):

        if title is None or title.strip() == "":
            return None
        
        return self.repository.create_new(title)

    def update_task(self, task_id, title=None, done=None):

        if title is None and done is None:
            return "empty"

        if title is not None and title.strip() == "":
            return "invalid_title"

        task = self.repository.get_by_id(task_id)

        if task is None:
            return "not_found"

        result =  self.repository.update(task_id,title,done)

        if result is None:
            return "not_found"

        return result

    def delete_task(self, task_id):
        task = self.repository.get_by_id(task_id)

        if task is None:
            return False

        return self.repository.delete(task_id)
    