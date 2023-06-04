from fastapi import HTTPException
from pydantic import BaseModel, validator

from schemas.users import TokenAuth

from utils.main import check_title

class Category(BaseModel):
  id: str  # Category ID
  title: str # Category title
  color_id: str # Category's color ID
  creator_id: str # Category's creator

class GetCategory(BaseModel):
  id: str
  title: str
  color: str
  color_id: str
  creator_id: str
  projects: int

class CreateCategory(BaseModel):
  title: str
  color_id: str
  creator: TokenAuth

  @validator("title")
  def validate_title(val):
    if check_title(val) == False: raise HTTPException(status_code=422, detail="Недопустимая длина названия категории")
    return val

  @validator("color_id")
  def validate_color(val):
    if len(val) == 0: raise HTTPException(status_code=422, detail="Не выбран цвет")
    return val

class ChangeCategory(BaseModel):
  id: str
  title: str
  color_id: str
  creator: TokenAuth

  @validator("title")
  def validate_title(val):
    if check_title(val) == False: raise HTTPException(status_code=422, detail="Недопустимая длина названия категории")
    return val

class DeleteCategory(BaseModel):
  id: str
  creator: TokenAuth