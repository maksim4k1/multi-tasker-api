from fastapi import HTTPException
from uuid import uuid4

from schemas.categories import Category, GetCategory, CreateCategory, ChangeCategory, DeleteCategory
from schemas.colors import Color
from schemas.users import User
from schemas.projects import Project
from schemas.tasks import Task
from schemas.subtasks import Subtask

from db.categories import get_categories, find_category, add_category, change_category, delete_category
from db.projects import delete_project, get_projects_by_category, get_projects_count_by_category
from db.tasks import delete_task, get_tasks_by_category
from db.subtasks import delete_subtask, get_subtasks_by_category

from services.users import users_service
from services.colors import colors_service

class CategoriesService:
  # get_categories
  def get_categories(self) -> list[GetCategory]:
    categories: list[Category] = get_categories()
    mapped_categories: list[GetCategory] = list(map(lambda item: self._convert_to_get_category(item), categories))
    return mapped_categories

  # get_category
  def get_category(self, id: str) -> GetCategory:
    category: Category = find_category(id)
    if category == None:
      raise HTTPException(status_code=404, detail="Категория не найдена")
    return self._convert_to_get_category(category)

  # create_category
  def create_category(self, data: CreateCategory) -> str:
    color: Color = colors_service.get_color(data.color_id)
    if color == None:
      raise HTTPException(status_code=404, detail="Цвет не найден")
    
    user: User = users_service._token_auth(data.creator)
    if user == None:
      raise HTTPException(status_code=404, detail="Пользователь не найден")

    new_category: Category = Category(
      id=str(uuid4()),
      title=data.title,
      color_id=data.color_id,
      creator_id=user.id
    )
    add_category(new_category)
    return new_category.id

  # change_category
  def change_category(self, data: ChangeCategory) -> str:
    user: User = users_service._token_auth(data.creator)
    if user == None:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")
      
    category: Category = find_category(data.id)
    if category == None:
      raise HTTPException(status_code=404, detail="Категория не найдена")

    if users_service._check_admin(user) == False and user.id != category.creator_id:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")
    category.title = data.title
    category.color_id = data.color_id
    change_category(category)
    return category.id

  # delete_category
  def delete_category(self, data: DeleteCategory):
    user: User = users_service._token_auth(data.creator)
    if user == None:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")

    print(data)
    category: Category = find_category(data.id)
    if category == None:
      raise HTTPException(status_code=404, detail="Категория не найдена")

    if users_service._check_admin(user) == False and user.id != category.creator_id:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")

    projects: list[Project] = get_projects_by_category(data.id)
    tasks: list[Task] = get_tasks_by_category(data.id)
    subtasks: list[Subtask] = get_subtasks_by_category(category.id)
    for project in projects: delete_project(project.id)
    for task in tasks: delete_task(task.id)
    for subtask in subtasks: delete_subtask(subtask.id)

    delete_category(data.id)
    return data.id

  # _convert_to_get_category
  def _convert_to_get_category(self, data: Category) -> GetCategory:
    projects: int = get_projects_count_by_category(data.id)
    return GetCategory(
      id=data.id,
      title=data.title,
      color_id=data.color_id,
      color=colors_service.get_color(data.color_id).color_hex,
      creator_id=data.creator_id,
      projects=projects
    )

categories_service: CategoriesService = CategoriesService()