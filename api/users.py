from fastapi import APIRouter

from schemas.users import UserProfile, CheckEmail, RegisterUser, LoginUser, ChangeUserUsername, ChangeUserEmail, ChangeUserPassword, ChangeUserPhoto, ChangeUserRole, TokenAuth, SetNewPassword, CheckCode, LoginUserProfile
from services.users import users_service

router = APIRouter()

# GET
# get_user
@router.get(
  "/api/users/user/{data}",
  status_code=200,
  response_model=UserProfile
)
def get_user(data: str):
  return users_service.get_user(data)

# filter_users_by_substr
@router.get(
  "/api/users/filter_by_substring/{substring}",
  status_code=200,
  response_model=list[UserProfile]
)
def filter_users_by_substr(substring: str):
  return users_service.filter_users_by_substr(substring)

# POST
# register_user
@router.post(
  "/api/users/register",
  status_code=200,
  response_model=LoginUserProfile
)
def register_user(data: RegisterUser):
  return users_service.register_user(data)

# login_user
@router.post(
  "/api/users/login",
  status_code=200,
  response_model=LoginUserProfile
)
def login_user(data: LoginUser):
  return users_service.login_user(data)

# logout_user
@router.post(
  "/api/users/logout",
  status_code=200,
  response_model=str
)
def logout_user(data: TokenAuth):
  return users_service.logout_user(data)

# user_password_recovery_get_email
@router.post(
  "/api/users/password_recovery/check_email",
  status_code=200,
  response_model=str
)
def user_password_recovery_get_email(data: CheckEmail):
  return users_service.user_password_recovery_get_email(data)

# user_password_recovery_get_code
@router.post(
  "/api/users/password_recovery/check_code",
  status_code=200,
  response_model=CheckCode
)
def user_password_recovery_get_code(code: CheckCode):
  return users_service.user_password_recovery_get_code(code)

# PATCH
# user_password_recovery_change_password
@router.patch(
  "/api/users/password_recovery/change_password",
  status_code=200,
  response_model=str
)
def user_password_recovery_change_password(data: SetNewPassword):
  return users_service.user_password_recovery_change_password(data)

# change_username
@router.patch(
  "/api/users/change/username",
  status_code=200,
  response_model=str
)
def change_username(data: ChangeUserUsername):
  return users_service.change_username(data)

# change_email
@router.patch(
  "/api/users/change/email",
  status_code=200,
  response_model=str
)
def change_email(data: ChangeUserEmail):
  return users_service.change_email(data)

# change_photo
@router.patch(
  "/api/users/change/photo",
  status_code=200,
  response_model=str
)
def change_photo(data: ChangeUserPhoto):
  return users_service.change_photo(data)

# change_password
@router.patch(
  "/api/users/change/password",
  status_code=200,
  response_model=str
)
def change_password(data: ChangeUserPassword):
  return users_service.change_password(data)

# change_role
@router.patch(
  "/api/users/change/role",
  status_code=200,
  response_model=str
)
def change_role(data: ChangeUserRole):
  return users_service.change_role(data)