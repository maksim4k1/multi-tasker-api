from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas.users import User, Token, Creds

Base = declarative_base()

class TableUser(Base):
  __tablename__ = "users"

  id = Column("id", String, primary_key=True)
  token = Column("token", String)
  token_expires = Column("token_expires", Integer)
  email = Column("email", String)
  password = Column("password", String)
  username = Column("username", String)
  photo = Column("photo", String)
  role = Column("role", String)
  code = Column("code", String)

  def __init__(self, id, token, token_expires, email, password, username, photo, role, code):
    self.id = id
    self.token = token
    self.token_expires = token_expires
    self.email = email
    self.password = password
    self.username = username
    self.photo = photo
    self.role = role
    self.code = code

engine = create_engine("sqlite:///db/db/users.db")
Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)()

def convert_to_user(user: TableUser) -> User:
  return User(
    id=user.id,
    token=Token(
      token=user.token,
      expires=user.token_expires
    ),
    auth=Creds(
      email=user.email,
      password=user.password
    ),
    username=user.username,
    photo=user.photo,
    role=user.role,
    code=user.code
  )

def convert_to_table_user(user: User) -> TableUser:
  return TableUser(
    id=user.id,
    token=user.token.token,
    token_expires=user.token.expires,
    email=user.auth.email,
    password=user.auth.password,
    username=user.username,
    photo=user.photo,
    role=user.role,
    code=user.code
  )

def get_users() -> list[User]:
  query = session.query(TableUser).all()
  users = []
  for user in query:
    if user != None: users.append(convert_to_user(user))
  return users

def filter_users_by_substr(substr: str) -> list[User]:
  query = session.query(TableUser).filter(or_(TableUser.email.ilike("%"+substr+"%"), TableUser.username.ilike("%"+substr+"%")))
  users = []
  for user in query:
    if user != None: users.append(convert_to_user(user))
  return users

def find_user(data: str) -> User:
  query = session.query(TableUser).filter(or_(TableUser.id == data, TableUser.email == data, TableUser.token == data)).first()
  if query == None: return None
  user = convert_to_user(query)
  
  return user

def add_user(user: User) -> User:
  session.add(convert_to_table_user(user))
  session.commit()
  return user

def change_user(user: User) -> User:
  session.begin_nested()
  query = session.query(TableUser).get(user.id)
  if query == None: return None
  query.token = user.token.token
  query.token_expires = user.token.expires
  query.email = user.auth.email
  query.password = user.auth.password
  query.username = user.username
  query.photo = user.photo
  query.role = user.role
  query.code = user.code

  session.commit()
  return user