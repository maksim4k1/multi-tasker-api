from fastapi import HTTPException
from pydantic import BaseModel, validator

from schemas.users import TokenAuth, UserProfile
from schemas.categories import GetCategory

from utils.main import check_title, check_description, get_ms_date, check_importance, convert_date_to_ms

class TaskCategory(BaseModel):
  id: str
  title: str
  color: str

class Task(BaseModel):
  id: str
  title: str  
  description: str
  importance: str
  completed: bool
  executor_id: str
  author_id: str
  deadline: int
  created: int
  updated: int
  category_id: str
  project_id: str

class GetTask(BaseModel):
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
  count_of_subtasks: int

class CreateTask(BaseModel):
  title: str
  description: str
  importance: str
  executor_email: str
  deadline: str
  project_id: str
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

class ChangeTask(BaseModel):
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

class CompleteTask(BaseModel):
  id: str
  completed: bool
  executor: TokenAuth

class DeleteTask(BaseModel):
  id: str
  author: TokenAuth