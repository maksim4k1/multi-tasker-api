from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas.projects import Project

Base = declarative_base()

class TableProject(Base):
  __tablename__ = "projects"

  id = Column("id", String, primary_key=True)
  title = Column("title", String)
  category_id = Column("category_id", String)
  creator_id = Column("creator_id", String)

  def __init__(self, id, title, category_id, creator_id):
    self.id = id
    self.title = title
    self.category_id = category_id
    self.creator_id = creator_id

engine = create_engine("sqlite:///db/db/projects.db")
Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)()

def convert_to_table_project(project: Project) -> TableProject:
  return TableProject(
    id=project.id,
    title=project.title,
    category_id=project.category_id,
    creator_id=project.creator_id
  )

def convert_to_project(project: TableProject) -> Project:
  return Project(
    id=project.id,
    title=project.title,
    category_id=project.category_id,
    creator_id=project.creator_id
  )

def get_projects_count_by_category(category_id: str) -> int:
  query = session.query(TableProject).filter(TableProject.category_id == category_id)
  count: int = 0
  for project in query:
    if project != None: count += 1
  return count

def get_projects_by_category(category_id: str) -> list[Project]:
  query = session.query(TableProject).filter(TableProject.category_id == category_id)
  projects = []
  for project in query:
    if project != None: projects.append(convert_to_project(project))
  return projects

def find_project(id: str) -> Project:
  query = session.query(TableProject).get(id)
  if query == None: return None
  project = convert_to_project(query)
  return project

def add_project(project: Project) -> Project:
  session.add(convert_to_table_project(project))
  session.commit()
  return project

def change_project(project: Project) -> Project:
  query = session.query(TableProject).get(project.id)
  if query == None: return None
  query.title = project.title
  session.commit()
  return project

def delete_project(project_id: str) -> str:
  query = session.query(TableProject).get(project_id)
  if query == None: return None
  session.delete(query)

  session.commit()
  return project_id