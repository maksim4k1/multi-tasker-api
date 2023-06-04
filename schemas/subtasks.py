from fastapi import HTTPException
from pydantic import BaseModel, validator

from schemas.users import UserProfile, TokenAuth
from schemas.tasks import Task, CreateTask, TaskCategory

from utils.main import check_importance, check_title, check_description, get_ms_date, convert_date_to_ms

class SubtaskTaskInfo(BaseModel):
  id: str
  title: str
  importance: str
  executor: UserProfile

class Subtask(Task):
  task_id: str

class GetSubtask(BaseModel):
  id: str
  title: str
  description: str
  importance: str
  completed: bool
  executor: UserProfile
  author: UserProfile
  deadline: str
  created: str
  updated: str
  category: TaskCategory
  project_id: str
  task: SubtaskTaskInfo

class CreateSubtask(BaseModel):
  title: str
  description: str
  importance: str
  executor_email: str
  deadline: str
  task_id: str
  author: TokenAuth

  @validator("title")
  def validate_title(val):
    if check_title(val) == False: raise HTTPException(status_code=422, detail="Недопустимая длина названия задачи")
    return val

class ChangeSubtask(BaseModel):
  id: str
  title: str
  description: str
  importance: str
  executor_email: str
  deadline: str
  author: TokenAuth

  @validator("title")
  def validate_title(val):
    if check_title(val) == False: raise HTTPException(status_code=422, detail="Недопустимая длина названия задачи")
    return val

  @validator("description")
  def validate_description(val):
    if check_description(val) == False: raise HTTPException(status_code=422, detail="Недопустимая длина описания задачи")
    return val

  @validator("deadline")
  def validate_deadline(val):
    if convert_date_to_ms(val) + (1000*60*60*24) < get_ms_date(): raise HTTPException(status_code=422, detail="Некорректно поставлен дедлайн")
    return val

  @validator("importance")
  def validate_importance(val):
    if check_importance(val) == False: raise HTTPException(status_code=422, detail="Некорректно введена важность")
    return val

class CompleteSubtask(BaseModel):
  id: str
  completed: bool
  executor: TokenAuth

class DeleteSubtask(BaseModel):
  id: str
  author: TokenAuth