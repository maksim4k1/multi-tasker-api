from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas.categories import Category

Base = declarative_base()

class TableCategory(Base):
  __tablename__ = "categories"

  id = Column("id", String, primary_key=True)
  title = Column("title", String)
  color_id = Column("color_id", String)
  creator_id = Column("creator_id", String)

  def __init__(self, id, title, color_id, creator_id):
    self.id = id
    self.title = title
    self.color_id = color_id
    self.creator_id = creator_id

engine = create_engine("sqlite:///db/db/categories.db")
Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)()

def convert_to_category(category: TableCategory) -> Category:
  return Category(
    id=category.id,
    title=category.title,
    color_id=category.color_id,
    creator_id=category.creator_id
  )

def convert_to_table_category(category: Category) -> TableCategory:
  return TableCategory(
    id=category.id,
    title=category.title,
    color_id=category.color_id,
    creator_id=category.creator_id
  )

def get_categories() -> list[Category]:
  query = session.query(TableCategory).all()
  categories = []
  for category in query:
    if category != None: categories.append(convert_to_category(category))
  return categories

def find_category(id: str) -> Category:
  query = session.query(TableCategory).get(id)
  if query == None: return None
  category = convert_to_category(query)
  return category

def add_category(category: Category) -> Category:
  session.add(convert_to_table_category(category))
  session.commit()
  return category

def change_category(category: Category) -> Category:
  query = session.query(TableCategory).get(category.id)
  if query == None: return None
  query.title = category.title
  query.color_id = category.color_id

  session.commit()
  return category

def delete_category(category_id: str) -> str:
  query = session.query(TableCategory).get(category_id)
  if query == None: return None
  session.delete(query)

  session.commit()
  return category_id