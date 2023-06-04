from pydantic import BaseModel

from schemas.users import TokenAuth

class Color(BaseModel):
  id: str # Color ID
  color_hex: str # Color's HEX

class AddColor(BaseModel):
  color_hex: str
  user: TokenAuth

class ChangeColor(BaseModel):
  id: str
  color_hex: str
  user: TokenAuth

class DeleteColor(BaseModel):
  id: str
  user: TokenAuth