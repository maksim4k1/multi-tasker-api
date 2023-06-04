from pydantic import BaseModel

from schemas.users import TokenAuth

class Project(BaseModel):
  id: str # Project ID
  title: str # Project Name
  category_id: str # Project's category
  creator_id: str # Project's creator

class GetProject(BaseModel):
  id: str
  title: str
  category_id: str
  category: str
  color: str
  creator_id: str
  count_of_tasks: int

class CreateProject(BaseModel):
  title: str
  category_id: str
  creator: TokenAuth

class ChangeProject(BaseModel):
  id: str
  title: str
  creator: TokenAuth

class DeleteProject(BaseModel):
  id: str
  creator: TokenAuth