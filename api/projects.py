from fastapi import APIRouter

from schemas.projects import GetProject, CreateProject, ChangeProject, DeleteProject

from services.projects import projects_service

router = APIRouter()

# GET
# get_project
@router.get(
  "/api/projects/get/{id}",
  status_code=200,
  response_model=GetProject
)
def get_project(id: str):
  return projects_service.get_project(id)

# get_projects_by_category
@router.get(
  "/api/projects/get/filter_by_category/{category_id}",
  status_code=200,
  response_model=list[GetProject]
)
def get_projects_by_category(category_id: str):
  return projects_service.get_projects_by_category(category_id)

# POST
# create_project
@router.post(
  "/api/projects/create",
  status_code=200,
  response_model=str
)
def create_project(data: CreateProject):
  return projects_service.create_project(data)

# PUT
# change_project
@router.put(
  "/api/projects/change",
  status_code=200,
  response_model=str
)
def change_project(data: ChangeProject):
  return projects_service.change_project(data)

# DELETE
# delete_project
@router.delete(
  "/api/projects/delete",
  status_code=200,
  response_model=str
)
def delete_project(data: DeleteProject):
  return projects_service.delete_project(data)