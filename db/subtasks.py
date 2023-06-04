from sqlalchemy import create_engine, Column, String, Integer, Boolean, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas.subtasks import Subtask
from schemas.assigned import FilterTasks

Base = declarative_base()

class TableSubtask(Base):
  __tablename__ = "subtasks"

  id=Column("id", String, primary_key=True)
  title=Column("title", String)
  description=Column("description", String)
  importance=Column("importance", Integer)
  completed=Column("completed", Boolean)
  executor_id=Column("executor_id", String)
  author_id=Column("author_id", String)
  deadline=Column("deadline", Integer)
  created=Column("created",  Integer)
  updated=Column("updated", Integer)
  category_id=Column("category_id", String)
  project_id=Column("project_id", String)
  task_id=Column("task_id", String)

  def __init__(self, id, title, description, importance, completed, executor_id, author_id, deadline, created, updated, project_id, category_id, task_id):
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
    self.task_id=task_id

engine = create_engine("sqlite:///db/db/subtasks.db")
Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)()

def convert_to_table_subtask(data: Subtask) -> TableSubtask:
  return TableSubtask(
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
    category_id=data.category_id,
    project_id=data.project_id,
    task_id=data.task_id
  )

def convert_to_subtask(data: TableSubtask) -> Subtask:
  return Subtask(
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
    category_id=data.category_id,
    project_id=data.project_id,
    task_id=data.task_id
  )

def covert_query_to_subtasks_list(query) -> list[Subtask]:
  subtasks: list[subtask] = []
  for subtask in query:
    if subtask != None: subtasks.append(convert_to_subtask(subtask))
  return subtasks

def filter_subtasks(user_id: str) -> list[Subtask]:
  query = session.query(TableSubtask).filter(TableSubtask.executor_id == user_id)
  return covert_query_to_subtasks_list(query)

def get_subtasks_by_category(category_id: str) -> list[Subtask]:
  query = session.query(TableSubtask).filter(TableSubtask.category_id == category_id)
  return covert_query_to_subtasks_list(query)

def get_subtasks_by_project(project_id: str) -> list[Subtask]:
  query = session.query(TableSubtask).filter(TableSubtask.project_id == project_id)
  return covert_query_to_subtasks_list(query)

def get_subtasks_by_task(task_id: str) -> list[Subtask]:
  query = session.query(TableSubtask).filter(TableSubtask.task_id == task_id)
  return covert_query_to_subtasks_list(query)

def get_subtasks_count_by_task(task_id: str) -> int:
  query = session.query(TableSubtask).filter(TableSubtask.task_id == task_id)
  count: int = 0
  for subtask in query:
    if subtask != None: count += 1
  return count

def find_subtask(subtask_id: str) -> Subtask:
  query = session.query(TableSubtask).get(subtask_id)
  if query == None: return None
  subtask = convert_to_subtask(query)
  return subtask

def add_subtask(subtask: Subtask) -> Subtask:
  session.add(convert_to_table_subtask(subtask))
  session.commit()
  return subtask

def change_subtask(subtask: Subtask) -> Subtask:
  query = session.query(TableSubtask).get(subtask.id)
  if query == None: return None
  query.title = subtask.title
  query.description = subtask.description
  query.importance = subtask.importance
  query.completed = subtask.completed
  query.executor_id = subtask.executor_id
  query.deadline = subtask.deadline
  query.updated = subtask.updated

  session.commit()
  return subtask

def delete_subtask(subtask_id: str) -> str:
  query = session.query(TableSubtask).get(subtask_id)
  if query == None: return None
  session.delete(query)

  session.commit()
  return subtask_id