from fastapi import HTTPException
from uuid import uuid4

from schemas.subtasks import Subtask, GetSubtask, ChangeSubtask, CreateSubtask, DeleteSubtask, CompleteSubtask, SubtaskTaskInfo
from schemas.tasks import GetTask, TaskCategory
from schemas.users import UserProfile, User
from schemas.categories import GetCategory
from schemas.projects import GetProject

from db.subtasks import find_subtask, get_subtasks_by_category, get_subtasks_by_project, get_subtasks_by_task, add_subtask, change_subtask, delete_subtask
from db.users import find_user

from services.users import users_service
from services.categories import categories_service
from services.projects import projects_service
from services.tasks import tasks_service

from utils.main import get_ms_date, convert_ms_to_date, convert_ms_to_date_with_hours, send_email, check_email, calculate_importance, convert_date_to_ms

class SubtasksService:
  # get_subtask
  def get_subtask(self, id: str) -> GetSubtask:
    subtask: Subtask = find_subtask(id)
    if subtask == None:
      raise HTTPException(status_code=404, detail="Подзадача не найдена")
    return self._convert_to_get_subtask(subtask)

  # get_subtasks_by_category
  def get_subtasks_by_category(self, category_id: str) -> int:
    category: GetCategory = categories_service.get_category(category_id)
    subtasks: list[Subtask] = get_subtasks_by_category(category.id)
    mapped_subtasks: list[GetSubtask] = list(map(lambda item: self._convert_to_get_subtask(item), subtasks))
    return mapped_subtasks

  # get_subtasks_by_project
  def get_subtasks_by_project(self, project_id: str) -> int:
    project: GetProject = projects_service.get_project(project_id)
    subtasks: list[Subtask] = get_subtasks_by_project(project.id)
    mapped_subtasks: list[GetSubtask] = list(map(lambda item: self._convert_to_get_subtask(item), subtasks))
    return mapped_subtasks

  # get_subtasks_by_task
  def get_subtasks_by_task(self, task_id: str) -> int:
    task: GetProject = tasks_service.get_task(task_id)
    subtasks: list[Subtask] = get_subtasks_by_task(task.id)
    mapped_subtasks: list[GetSubtask] = list(map(lambda item: self._convert_to_get_subtask(item), subtasks))
    return mapped_subtasks

  # create_subtask
  def create_subtask(self, data: CreateSubtask) -> str:
    task: GetTask = tasks_service.get_task(data.task_id)
    author: UserProfile = users_service._token_auth(data.author)
    if author == None:
      raise HTTPException(status_code=404, detail="Пользователь не найден")

    executor_id: str = None
    executor: User = find_user(data.executor_email)
    if len(data.executor_email) == 0:
      executor_id = author.id
    elif executor == None:
      if check_email(data.executor_email) == False:
        raise HTTPException(status_code=400, detail="Некорректно введён Email исполнителя")
      send_email(
        email=data.executor_email,
        message_title="Приглашение в MULTI-TASKER",
        message="Здравствуйте, вы были приглашениы в приложение MULTI-TASKER\nСсылка на приложение: https:\multi-subtasker.com\download"
      )
      executor_id = data.executor_email
    else:
      executor_id = executor.id

    new_subtask: Subtask = Subtask(
      id=str(uuid4()),
      title=data.title,
      description=data.description,
      importance=data.importance,
      completed=False,
      executor_id=executor_id,
      author_id=author.id,
      deadline=convert_date_to_ms(data.deadline),
      created=get_ms_date(),
      updated=get_ms_date(),
      project_id=task.project_id,
      category_id=task.category.id,
      task_id=task.id
    )

    add_subtask(new_subtask)
    return new_subtask.id

  # change_subtask
  def change_subtask(self, data: ChangeSubtask) -> str:
    subtask: Subtask = find_subtask(data.id)
    if subtask == None:
      raise HTTPException(status_code=404, detail="Подзадача не найдена")
    user: User = users_service._token_auth(data.author)
    if user == None:
      raise HTTPException(status_code=404, detail="Пользователь не найден")
    if users_service._check_admin(user) == False and user.id != subtask.author_id:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")

    executor_id: str = None
    executor: User = find_user(data.executor_email)
    if len(data.executor_email) == 0:
      executor_id = subtask.author_id
    elif executor == None:
      if check_email(data.executor_email) == False:
        raise HTTPException(status_code=400, detail="Некорректно введён Email исполнителя")
      send_email(
        email=data.executor_email,
        message_title="Приглашение в MULTI-TASKER",
        message="Здравствуйте, вы были приглашениы в приложение MULTI-TASKER\nСсылка на приложение: https:\multi-subtasker.com\download"
      )
      executor_id = data.executor_email
    else:
      executor_id = executor.id

    subtask.title=data.title
    subtask.description=data.description
    subtask.importance=data.importance
    subtask.executor_id=executor_id
    subtask.deadline=convert_date_to_ms(data.deadline)
    subtask.updated=get_ms_date()

    change_subtask(subtask)
    return subtask.id

  # complete_subtask
  def complete_subtask(self, data: CompleteSubtask) -> str:
    subtask: Subtask = find_subtask(data.id)
    if subtask == None:
      raise HTTPException(status_code=404, detail="Подзадача не найдена")
    
    user: User = users_service._token_auth(data.executor)
    if user == None:
      raise HTTPException(status_code=404, detail="Пользователь не найден")

    if users_service._check_admin(user) == False and user.id != subtask.executor_id and user.id != subtask.author_id:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")

    subtask.completed = data.completed

    change_subtask(subtask)
    return subtask.id

  # delete_subtask
  def delete_subtask(self, data: DeleteSubtask) -> str:
    subtask: Subtask = find_subtask(data.id)
    if subtask == None:
      raise HTTPException(status_code=404, detail="Подзадача не найдена")
    
    user: User = users_service._token_auth(data.author)
    if user == None:
      raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if users_service._check_admin(user) == False and user.id != subtask.author_id:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")

    delete_subtask(subtask.id)
    return subtask.id

  # _convert_to_get_subtask
  def _convert_to_get_subtask(self, data: Subtask) -> GetSubtask:
    author: UserProfile = users_service.get_user(data.author_id)
    category: GetCategory = categories_service.get_category(data.category_id)
    project: GetProject = projects_service.get_project(data.project_id)
    task: GetTask = tasks_service.get_task(data.task_id)
    importance: str = data.importance
    if len(importance) == 0:
      importance = calculate_importance(data.deadline)

    executor: UserProfile = None
    if len(data.executor_id) == 0:
      executor = author
    elif check_email(data.executor_id) == True and find_user(data.executor_id) == None:
      executor = UserProfile( id="", username="", email=data.executor_id, photo="")
    else:
      executor = users_service.get_user(data.executor_id)

    return GetSubtask(
      id=data.id,
      title=data.title,
      description=data.description,
      importance=importance,
      executor=executor,
      completed=data.completed,
      author=author,
      deadline=convert_ms_to_date(data.deadline),
      created=convert_ms_to_date_with_hours(data.created),
      updated=convert_ms_to_date_with_hours(data.updated),
      project_id=project.id,
      category=TaskCategory(
        id=category.id,
        title=category.title,
        color=category.color
      ),
      task=SubtaskTaskInfo(
        id=task.id,
        title=task.title,
        importance=task.importance,
        executor=UserProfile(
          id=task.executor.id,
          email=task.executor.email,
          username=task.executor.username,
          photo=task.executor.photo
        )
      )
    )

subtasks_service: SubtasksService = SubtasksService()