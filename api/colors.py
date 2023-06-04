from fastapi import APIRouter

from schemas.colors import Color, AddColor, ChangeColor, DeleteColor
from services.colors import colors_service

router = APIRouter()

# GET
# get_colors
@router.get(
  "/api/colors/get",
  status_code=200,
  response_model=list[Color]
)
def get_colors():
  return colors_service.get_colors()

# POST
# add_color
@router.post(
  "/api/colors/add",
  status_code=200,
  response_model=str
)
def add_color(data: AddColor):
  return colors_service.add_color(data)

# PUT
# change_color
@router.put(
  "/api/colors/change",
  status_code=200,
  response_model=str
)
def change_color(data: ChangeColor):
  return colors_service.change_color(data)

# DELETE
# delete_color
@router.delete(
  "/api/colors/delete",
  status_code=200,
  response_model=str
)
def delete_color(data: DeleteColor):
  return colors_service.delete_color(data)