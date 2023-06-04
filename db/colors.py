from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas.colors import Color

Base = declarative_base()

class TableColor(Base):
  __tablename__ = "colors"

  id = Column("id", String, primary_key=True)
  color_hex = Column("color_hex", String)

  def __init__(self, id, color_hex):
    self.id = id
    self.color_hex = color_hex

engine = create_engine("sqlite:///db/db/colors.db")
Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)()

def convert_to_color(color: TableColor) -> Color:
  return Color(
    id=color.id,
    color_hex=color.color_hex
  )

def convert_to_table_color(color: Color) -> TableColor:
  return TableColor(
    id=color.id,
    color_hex=color.color_hex
  )

def get_colors() -> list[Color]:
  query = session.query(TableColor).all()
  categories = []
  for color in query:
    if color != None: categories.append(convert_to_color(color))
  return categories

def find_color(id: str) -> Color:
  color = session.query(TableColor).get(id)
  if color == None: return None
  return convert_to_color(color)

def add_color(color: Color) -> Color:
  session.add(convert_to_table_color(color))
  session.commit()
  return color

def change_color(color: Color) -> Color:
  query = session.query(TableColor).get(color.id)
  if query == None: return None
  query.color_hex = color.color_hex

  session.commit()
  return color

def delete_color(color_id: str) -> str:
  query = session.query(TableColor).get(color_id)
  if query == None: return None
  session.delete(query)

  session.commit()
  return color_id