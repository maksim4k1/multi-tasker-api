from fastapi import HTTPException
from uuid import uuid4

from schemas.colors import Color, AddColor, ChangeColor, DeleteColor
from schemas.users import User
from schemas.categories import Category

from db.colors import get_colors, find_color, add_color, change_color, delete_color
from db.categories import change_category, get_categories

from services.users import users_service

class ColorsService:
  # get_colors
  def get_colors(self) -> list[Color]:
    colors: list[Color] = get_colors()
    return colors

  # get_color
  def get_color(self, id: str) -> Color:
    color: Color = find_color(id)
    if color == None:
      raise HTTPException(status_code=404, detail="Цвет не найден")
    return color

  # create_color
  def add_color(self, data: AddColor) -> str:
    user: User = users_service._token_auth(data.user)
    if user == None or users_service._check_admin(user) == False:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")

    color: Color = Color(
      id=str(uuid4()),
      color_hex=data.color_hex,
      user=data.user
    )
    add_color(color)
    return color.id

  # change_color
  def change_color(self, data: ChangeColor) -> str:
    user: User = users_service._token_auth(data.user)
    if user == None or users_service._check_admin(user) == False:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")
      
    color: Color = find_color(data.id)
    if color == None:
      raise HTTPException(status_code=404, detail="Цвет не найден")
    color.color_hex = data.color_hex
    change_color(color)
    return color.id

  # delete_color
  def delete_color(self, data: DeleteColor):
    colors: list[Color] = get_colors()
  
    user: User = users_service._token_auth(data.user)
    if user == None or users_service._check_admin(user) == False:
      raise HTTPException(status_code=403, detail="Вы не можете выполнить это действие")

    if len(colors) <= 1:
      raise HTTPException(status_code=406, detail="В базе данных должен остаться хотябы один элемент")

    color: Color = find_color(data.id)
    if color == None:
      raise HTTPException(status_code=404, detail="Цвет не найден")
    
    delete_color(data.id)
    colors = get_colors()

    categories: list[Category] = get_categories()
    for category in categories:
      category.color_id = colors[0].id
      change_category(category)
    return data.id

colors_service: ColorsService = ColorsService()