from fastapi import HTTPException
from uuid import uuid4

from schemas.tasks import Task, GetTask, ChangeTask, CreateTask, DeleteTask, CompleteTask, TaskCategory
from schemas.users import UserProfile, User
from schemas.categories import GetCategory
from schemas.projects import GetProject
from schemas.subtasks import Subtask

from db.tasks import find_task, get_tasks_by_category, get_tasks_by_project, add_task, change_task, delete_task
from db.users import find_user
from db.subtasks import get_subtasks_count_by_task, get_subtasks_by_task, delete_subtask

from services.users import users_service
from services.categories import categories_service
from services.projects import projects_service

from utils.main import get_ms_date, convert_ms_to_date, convert_ms_to_date_with_hours, send_email, check_email, calculate_importance, convert_date_to_ms

class TasksService:
  # get_task
  def get_task(self, id: str) -> GetTask:
    task: Task = find_task(id)
    if task == None:
      raise HTTPException(status_code=404, detail="Задача не найдена")
    return self._convert_to_get_task(task)

  # get_tasks_by_category
  def get_tasks_by_category(self, category_id: str) -> int:
    category: GetCategory = categories_service.get_category(category_id)
    tasks: list[Task] = get_tasks_by_category(category.id)
    mapped_tasks: list[GetTask] = list(map(lambda item: self._convert_to_get_task(item), tasks))
    return mapped_tasks

  # get_tasks_by_project
  def get_tasks_by_project(self, project_id: str) -> int:
    project: GetProject = projects_service.get_project(project_id)
    tasks: list[Task] = get_tasks_by_project(project.id)
    mapped_tasks: list[GetTask] = list(map(lambda item: self._convert_to_get_task(item), tasks))
    return mapped_tasks

  # create_task
  def create_task(self, data: CreateTask) -> str:
    project: GetProject = projects_service.get_project(data.project_id)
    author: UserProfile = users_service._token_auth(data.author)
    if project.category_id != project.category_id:
      raise HTTPException(status_code=400, detail="Проект не принадлежит выбранной категории")
    if author == None:
      raise HTTPException(status_code=404, detail="Такой пользователь не найден")

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
        message="Здравствуйте, вы были приглашениы в приложение MULTI-TASKER\nСсылка на приложение: https:\multi-tasker.com\download"
      )
      executor_id = data.executor_email
    else:
      executor_id = executor.id

    new_task: Task = Task(
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
      project_id=project.id,
      category_id=project.category_id,
    )

    add_task(new_task)
    return new_task.id

  # change_task
  def change_task(self, data: ChangeTask) -> str:
    task: Task = find_task(data.id)
    if task == None:
      raise HTTPException(status_code=404, detail="Задача не найдена")
    user: User = users_service._token_auth(data.author)
    if user == None:
      raise HTTPException(status_code=404, detail="Такой пользователь не найден")
    if users_service._check_admin(user) == False and user.id != task.author_id:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")

    executor_id: str = None
    executor: User = find_user(data.executor_email)
    if len(data.executor_email) == 0:
      executor_id = task.author_id
    elif executor == None:
      if check_email(data.executor_email) == False:
        raise HTTPException(status_code=400, detail="Некорректно введён Email исполнителя")
      send_email(
        email=data.executor_email,
        message_title="Приглашение в MULTI-TASKER",
        message="Здравствуйте, вы были приглашениы в приложение MULTI-TASKER\nСсылка на приложение: https:\multi-tasker.com\download"
      )
      executor_id = data.executor_email
    else:
      executor_id = executor.id

    task.title=data.title
    task.description=data.description
    task.importance=data.importance
    task.executor_id=executor_id
    task.deadline=convert_date_to_ms(data.deadline)
    task.updated=get_ms_date()

    change_task(task)
    return task.id

  # complete_task
  def complete_task(self, data: CompleteTask) -> str:
    task: Task = find_task(data.id)
    if task == None:
      raise HTTPException(status_code=404, detail="Задача не найдена")
    
    user: User = users_service._token_auth(data.executor)
    if user == None:
      raise HTTPException(status_code=404, detail="Такой пользователь не найден")

    if users_service._check_admin(user) == False and user.id != task.executor_id and user.id != task.author_id:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")

    task.completed = data.completed

    change_task(task)
    return task.id

  # delete_task
  def delete_task(self, data: DeleteTask) -> str:
    task: Task = find_task(data.id)
    if task == None:
      raise HTTPException(status_code=404, detail="Задача не найдена")
    
    user: User = users_service._token_auth(data.author)
    if user == None:
      raise HTTPException(status_code=404, detail="Такой пользователь не найден")
    
    if users_service._check_admin(user) == False and user.id != task.author_id:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")

    subtasks: list[Subtask] = get_subtasks_by_task(task.id)
    for subtask in subtasks: delete_subtask(subtask.id)

    delete_task(task.id)
    return task.id

  # _convert_to_get_task
  def _convert_to_get_task(self, data: Task) -> GetTask:
    author: UserProfile = users_service.get_user(data.author_id)
    category: GetCategory = categories_service.get_category(data.category_id)
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

    subtasks_count: int = get_subtasks_count_by_task(data.id)

    return GetTask(
      id=data.id,
      title=data.title,
      description=data.description,
      importance=importance,
      completed=data.completed,
      executor=executor,
      author=author,
      deadline=convert_ms_to_date(data.deadline),
      created=convert_ms_to_date_with_hours(data.created),
      updated=convert_ms_to_date_with_hours(data.updated),
      project_id=data.project_id,
      category=TaskCategory(
        id=category.id,
        title=category.title,
        color=category.color,
      ),
      count_of_subtasks=subtasks_count
    )

tasks_service: TasksService = TasksService()