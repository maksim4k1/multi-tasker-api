from fastapi import APIRouter

from schemas.subtasks import GetSubtask, CreateSubtask, ChangeSubtask, CompleteSubtask, DeleteSubtask

from services.subtasks import subtasks_service

router = APIRouter()

# GET
# get_subtask
@router.get(
  "/api/subtasks/get/{id}",
  status_code=200,
  response_model=GetSubtask
)
def get_subtask(id: str):
  return subtasks_service.get_subtask(id)

# get_subtasks_by_project
@router.get(
  "/api/subtasks/get/filter_by_task/{task_id}",
  status_code=200,
  response_model=list[GetSubtask]
)
def get_subtasks_by_task(task_id: str):
  return subtasks_service.get_subtasks_by_task(task_id)

# POST
# create_subtask
@router.post(
  "/api/subtasks/create",
  status_code=200,
  response_model=str
)
def create_subtask(data: CreateSubtask):
  return subtasks_service.create_subtask(data)

# PATCH
# complete_subtask
@router.patch(
  "/api/subtasks/complete",
  status_code=200,
  response_model=str
)
def complete_subtask(data: CompleteSubtask):
  return subtasks_service.complete_subtask(data)

# PUT
# change_subtask
@router.put(
  "/api/subtasks/change",
  status_code=200,
  response_model=str
)
def change_subtask(data: ChangeSubtask):
  return subtasks_service.change_subtask(data)

# DELETE
@router.delete(
  "/api/subtasks/delete",
  status_code=200,
  response_model=str
)
def delete_subtask(data: DeleteSubtask):
  return subtasks_service.delete_subtask(data)