from fastapi import APIRouter

from schemas.tasks import GetTask, CreateTask, ChangeTask, CompleteTask, DeleteTask

from services.tasks import tasks_service

router = APIRouter()

# GET
# get_task
@router.get(
  "/api/tasks/get/{id}",
  status_code=200,
  response_model=GetTask
)
def get_task(id: str):
  return tasks_service.get_task(id)

# get_tasks_by_project
@router.get(
  "/api/tasks/get/filter_by_project/{project_id}",
  status_code=200,
  response_model=list[GetTask]
)
def get_tasks_by_project(project_id: str):
  return tasks_service.get_tasks_by_project(project_id)

# POST
# create_task
@router.post(
  "/api/tasks/create",
  status_code=200,
  response_model=str
)
def create_task(data: CreateTask):
  return tasks_service.create_task(data)

# PATCH
# complete_task
@router.patch(
  "/api/tasks/complete",
  status_code=200,
  response_model=str
)
def complete_task(data: CompleteTask):
  return tasks_service.complete_task(data)

# PUT
# change_task
@router.put(
  "/api/tasks/change",
  status_code=200,
  response_model=str
)
def change_task(data: ChangeTask):
  return tasks_service.change_task(data)

# DELETE
@router.delete(
  "/api/tasks/delete",
  status_code=200,
  response_model=str
)
def delete_task(data: DeleteTask):
  return tasks_service.delete_task(data)