from fastapi import HTTPException
from uuid import uuid4

from schemas.projects import Project, GetProject, CreateProject, ChangeProject, DeleteProject
from schemas.categories import GetCategory
from schemas.users import User
from schemas.tasks import Task
from schemas.subtasks import Subtask

from db.projects import get_projects_by_category, add_project, find_project, change_project, delete_project
from db.tasks import delete_task, get_tasks_by_project, get_tasks_count_by_project
from db.subtasks import get_subtasks_by_project, delete_subtask

from services.users import users_service
from services.categories import categories_service

from utils.main import check_title

class ProjectsService:
  # get_projects_by_category
  def get_projects_by_category(self, category_id: str) -> list[GetProject]:
    projects: list[Project] = get_projects_by_category(category_id)
    mapped_projects: list[GetProject] = list(map(lambda item: self._convert_to_get_project(item), projects))
    return mapped_projects

  def get_project(self, id: str) -> GetProject:
    project: Project = find_project(id)
    if project == None:
      raise HTTPException(status_code=404, detail="Проект не найден")
    return self._convert_to_get_project(project)

  # create_project
  def create_project(self, data: CreateProject) -> str:
    if check_title(data.title) == False:
      raise HTTPException(status_code=400, detail="Недопустимая длина названия проекта")

    user: User = users_service._token_auth(data.creator)
    if user == None:
      raise HTTPException(status_code=404, detail="Пользователь не найден")

    category: GetCategory = categories_service.get_category(data.category_id)

    new_project: Project = Project(
      id=str(uuid4()),
      title=data.title,
      category_id=category.id,
      creator_id=user.id
    )
    add_project(new_project)
    return new_project.id

  # change_project
  def change_project(self, data: ChangeProject) -> str:
    if check_title(data.title) == False:
      raise HTTPException(status_code=400, detail="Недопустимая длина названия проекта")

    user: User = users_service._token_auth(data.creator)
    if user == None:
      raise HTTPException(status_code=404, detail="Пользователь не найден")

    project: Project = find_project(data.id)
    if project == None:
      raise HTTPException(status_code=404, detail="Проект не найден")

    if users_service._check_admin(user) == False and user.id != project.creator_id:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")
    project.title = data.title
    change_project(project)
    return project.id

  # delete_project
  def delete_project(self, data: DeleteProject) -> str:
    user: User = users_service._token_auth(data.creator)
    if user == None:
      raise HTTPException(status_code=404, detail="Пользователь не найден")

    project: Project = find_project(data.id)
    if project == None:
      raise HTTPException(status_code=404, detail="Проект не найден")

    if users_service._check_admin(user) == False and user.id != project.creator_id:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")

    tasks: list[Task] = get_tasks_by_project(project.id)
    subtasks: list[Subtask] = get_subtasks_by_project(project.id)
    for task in tasks: delete_task(task.id)
    for subtask in subtasks: delete_subtask(subtask.id)
    
    delete_project(project.id)
    return project.id

  # _convert_to_get_project
  def _convert_to_get_project(self, data: Project) -> GetProject:
    category: GetCategory = categories_service.get_category(data.category_id)
    tasks_count: int = get_tasks_count_by_project(data.id)
    return GetProject(
      id=data.id,
      title=data.title,
      category_id=category.id,
      category=category.title,
      color=category.color,
      creator_id=data.creator_id,
      count_of_tasks=tasks_count
    )

projects_service: ProjectsService = ProjectsService()