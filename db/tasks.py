from sqlalchemy import create_engine, Column, String, Integer, Boolean, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas.tasks import Task
from schemas.assigned import FilterTasks

from utils.main import calculate_importance

Base = declarative_base()

class TableTask(Base):
  __tablename__ = "tasks"

  id=Column("id", String, primary_key=True)
  title=Column("title", String)
  description=Column("description", String)
  importance=Column("importance", String)
  completed=Column("completed", Boolean)
  executor_id=Column("executor_id", String)
  author_id=Column("author_id", String)
  deadline=Column("deadline", Integer)
  created=Column("created",  Integer)
  updated=Column("updated", Integer)
  project_id=Column("project_id", String)
  category_id=Column("category_id", String)

  def __init__(self, id, title, description, importance, completed, executor_id, author_id, deadline, created, updated, project_id, category_id):
    self.id=id
    self.title=title
    self.description=description
    self.importance=importance
    self.completed=completed
    self.executor_id=executor_id
    self.author_id=author_id
    self.deadline=deadline
    self.created=created
    self.updated=updated
    self.project_id=project_id
    self.category_id=category_id

engine = create_engine("sqlite:///db/db/tasks.db")
Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)()

def convert_to_table_task(data: Task) -> TableTask:
  return TableTask(
    id=data.id,
    title=data.title,
    description=data.description,
    importance=data.importance,
    completed=data.completed,
    executor_id=data.executor_id,
    author_id=data.author_id,
    deadline=data.deadline,
    created=data.created,
    updated=data.updated,
    project_id=data.project_id,
    category_id=data.category_id
  )

def convert_to_task(data: TableTask) -> Task:
  return Task(
    id=data.id,
    title=data.title,
    description=data.description,
    importance=data.importance,
    completed=data.completed,
    executor_id=data.executor_id,
    author_id=data.author_id,
    deadline=data.deadline,
    created=data.created,
    updated=data.updated,
    project_id=data.project_id,
    category_id=data.category_id
  )

def covert_query_to_tasks_list(query) -> list[Task]:
  tasks: list[Task] = []
  for task in query:
    if task != None: tasks.append(convert_to_task(task))
  return tasks

def filter_tasks(user_id: str) -> list[Task]:
  query = session.query(TableTask).filter(TableTask.executor_id == user_id)
  return covert_query_to_tasks_list(query)

def get_tasks_by_category(category_id: str) -> list[Task]:
  query = session.query(TableTask).filter(TableTask.category_id == category_id)
  return covert_query_to_tasks_list(query)

def get_tasks_by_project(project_id: str) -> list[Task]:
  query = session.query(TableTask).filter(TableTask.project_id == project_id)
  return covert_query_to_tasks_list(query)

def get_tasks_count_by_project(project_id: str) -> int:
  query = session.query(TableTask).filter(TableTask.project_id == project_id)
  count: int = 0
  for task in query:
    if task != None: count += 1
  return count

def find_task(task_id: str) -> Task:
  query = session.query(TableTask).get(task_id)
  if query == None: return None
  task = convert_to_task(query)
  return task

def add_task(task: Task) -> Task:
  session.add(convert_to_table_task(task))
  session.commit()
  return task

def change_task(task: Task) -> Task:
  query = session.query(TableTask).get(task.id)
  if query == None: return None
  query.title = task.title
  query.description = task.description
  query.importance = task.importance
  query.completed = task.completed
  query.executor_id = task.executor_id
  query.deadline = task.deadline
  query.updated = task.updated

  session.commit()
  return task

def delete_task(task_id: str) -> str:
  query = session.query(TableTask).get(task_id)
  if query == None: return None
  session.delete(query)

  session.commit()
  return task_id