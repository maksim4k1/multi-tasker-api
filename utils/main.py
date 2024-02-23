from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# Constants
class ImportanceClass:
  very_important: str
  important: str
  low_important: str
  not_important: str

  def __init__(self, very_important, important, low_important, not_important):
    self.very_important=very_important
    self.important=important
    self.low_important=low_important
    self.not_important=not_important

Importance: ImportanceClass = ImportanceClass(
  very_important="very_important",
  important="important",
  low_important="low_important",
  not_important="not_important"
)

# Token
def get_token_expires():
  return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000) + (1000 * 60 * 60 * 24 * 3)

def check_token_expires(expires: int):
  return (expires - int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)) > 0

# Data Validation
def check_email(email: str) -> bool:
  if len(email) == 0: return True

  # A-Z a-z 0-9 - _ . @
  def is_ok(string):
    symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_.@'
    for letter in string:
      if letter not in symbols: return False
    return True
  
  dog_count = 0
  dot = False
  i = 0

  for letter in email:
    if letter == "@":
      if dog_count == 1 or (i+1 < len(email) and email[i+1] == ".") or i == 0: return False
      else: dog_count = 1
    if letter == "." and dog_count == 1:
      if i+1 == len(email): return False
      else:
        dot = True
    i += 1
  if dot == False or dog_count == 0: return False

  return is_ok(email)

def check_password(password: str) -> bool:
  if len(password) == 0: return True
  if 8 > len(password) or len(password) > 16: return False
  # A-Z a-z 0-9 ! # $ % & * + - . < = > ? @
  symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!#$%&*+-.<=>?@'
  for letter in password:
    if letter not in symbols: return False
  return True

def check_username(username: str) -> bool:
  if len(username) > 50: return False
  symbols = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
  for letter in username:
    if letter not in symbols: return False
  return True

def check_title(title: str) -> bool:
  if len(title) > 100 or len(title) == 0: return False
  return True

def check_description(description: str) -> bool:
  if len(description) > 10000: return False
  return True

# Email
def send_email(email: str, message: str, message_title: str) -> bool:
  sender: str = "email" # need to change
  sender_password: str = "password" # need to change

  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()

  try:
    server.login(sender, sender_password)
    msg = MIMEText(message)
    msg["Subject"] = message_title
    server.sendmail(sender, email, msg.as_string())

    return True
  except:
    raise ValueError("Пользователь с таким Email не найден")

def check_importance(importance: str) -> bool:
  if len(importance) != 0 and importance != Importance.very_important and importance != Importance.important and importance != Importance.low_important and importance != Importance.not_important:
    return False
  return True

# Dates
def get_ms_date():
  return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)

def convert_date_to_ms(data: str) -> int:
  return int((datetime.strptime(data, "%Y-%m-%d") - datetime(1970, 1, 1)).total_seconds() * 1000)

def convert_ms_to_simple_date(ms_date: int) -> str:
  date_time = datetime.fromtimestamp(ms_date // 1000)
  return date_time.strftime("%Y-%m-%d")

def convert_ms_to_date(ms_date: int) -> str:
  mounth: dict = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декарбря",
  }
  date = datetime.fromtimestamp(ms_date/1000.0)

  day: int = date.day
  mounth_num: int = date.month
  year: int = date.year

  return f"{day if day >= 10 else '0'+str(day)} {mounth[mounth_num]} {year}"

def convert_ms_to_date_with_hours(ms_date: int) -> str:
  date: datetime = datetime.fromtimestamp(ms_date/1000.0)

  hour: int = date.hour
  minute: int = date.minute
  return f"{convert_ms_to_date(ms_date)}, {hour if hour >= 10 else '0'+str(hour)}:{minute if minute >= 10 else '0'+str(minute)}"

def count_days(end: int, start: int = get_ms_date()) -> int:
  ms = end - start
  if ms <= 0: return 0

  days = ((ms / (1000*60*60*24)) // 1) - 1
  return days

def calculate_importance(deadline: int):
  days = count_days(deadline)
  if days >= 3:
    return Importance.not_important
  elif days >= 2:
    return Importance.low_important
  else:
    return Importance.very_important