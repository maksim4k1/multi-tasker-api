from fastapi import APIRouter

from schemas.categories import Category, CreateCategory, GetCategory, ChangeCategory, DeleteCategory
from services.categories import categories_service

router = APIRouter()

# GET
# get_category
@router.get(
  "/api/categories/get/{id}",
  status_code=200,
  response_model=GetCategory
)
def get_category(id: str):
  return categories_service.get_category(id)

# get_categories
@router.get(
  "/api/categories/get",
  status_code=200,
  response_model=list[GetCategory]
)
def get_categories():
  return categories_service.get_categories()

# POST
# create_category
@router.post(
  "/api/categories/create",
  status_code=200,
  response_model=str
)
def create_category(data: CreateCategory):
  return categories_service.create_category(data)

# PUT
# change_category
@router.put(
  "/api/categories/change",
  status_code=200,
  response_model=str
)
def change_category(data: ChangeCategory):
  return categories_service.change_category(data)

# DELETE
# delete_category
@router.delete(
  "/api/categories/delete",
  status_code=200,
  response_model=str
)
def delete_category(data: DeleteCategory):
  return categories_service.delete_category(data)