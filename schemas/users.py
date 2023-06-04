from fastapi import HTTPException
from pydantic import BaseModel, validator

from utils.main import check_password, check_email, check_username

class Creds(BaseModel):
  email: str
  password: str

  @validator("email")
  def validate_email(val):
    if check_email(val) == False: raise HTTPException(status_code=422, detail="Некорректно введён Email")
    return val

  @validator("password")
  def validate_password(val):
    if check_password(val) == False: raise HTTPException(status_code=422, detail="Некорректно введён пароль")
    return val

class Token(BaseModel):
  token: str
  expires: int

class TokenAuth(BaseModel):
  token: str

class User(BaseModel):
  id: str # User ID
  token: Token # User token info (token, token expires (number of milliseconds from 1970))
  auth: Creds # User credentaials (email, password)
  username: str # User username
  photo: str # User photo (base64)
  role: str # User role (author/user)
  code: str # Code, that sended to user's email

class UserProfile(BaseModel):
  id: str
  email: str
  username: str
  photo: str

class RegisterUser(BaseModel):
  auth: Creds
  check_password: str

  @validator("check_password")
  def validate_check_password(val):
    if check_password(val) == False: raise HTTPException(status_code=422, detail="Некорректно введён пароль")
    return val

class LoginUser(BaseModel):
  auth: Creds
  token_auth: TokenAuth

class LoginUserProfile(BaseModel):
  id: str
  email: str
  username: str
  photo: str
  token: str
  role: str

class CheckEmail(BaseModel):
  email: str

  @validator("email")
  def validate_email(val):
    if check_email(val) == False: raise HTTPException(status_code=422, detail="Некорректно введён Email")
    return val
    
class CheckCode(BaseModel):
  email: str
  code: str

  @validator("email")
  def validate_email(val):
    if check_email(val) == False: raise HTTPException(status_code=422, detail="Некорректно введён Email")
    return val

class NewPassword(BaseModel):
  new_password: str
  check_new_password: str

  @validator("new_password")
  def validate_new_password(val):
    if check_password(val) == False: raise HTTPException(status_code=422, detail="Некорректно введён пароль")
    return val
  
  @validator("check_new_password")
  def validate_check_new_password(val):
    if check_password(val) == False: raise HTTPException(status_code=422, detail="Некорректно введён пароль")
    return val

class SetNewPassword(BaseModel):
  email: str
  code: str
  new_password: NewPassword

  @validator("email")
  def validate_email(val):
    if check_email(val) == False: raise HTTPException(status_code=422, detail="Некорректно введён Email")
    return val

class ChangeUserUsername(BaseModel):
  username: str
  user: TokenAuth

  @validator("username")
  def validate_username(val):
    if check_username(val) == False: raise HTTPException(status_code=422, detail="Введены недопустимые символы")
    return val

class ChangeUserEmail(BaseModel):
  email: str
  user: TokenAuth

  @validator("email")
  def validate_email(val):
    if check_email(val) == False: raise HTTPException(status_code=422, detail="Некорректно введён Email")
    return val

class ChangeUserPassword(BaseModel):
  old_password: str
  new_password: NewPassword
  user: TokenAuth

  @validator("old_password")
  def validate_old_password(val):
    if check_password(val) == False: raise HTTPException(status_code=422, detail="Некорректно введён пароль")
    return val

class ChangeUserPhoto(BaseModel):
  photo: str
  user: TokenAuth

class ChangeUserRole(BaseModel):
  id: str
  role: str
  admin: TokenAuth