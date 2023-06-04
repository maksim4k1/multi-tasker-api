from pydantic import BaseModel

from schemas.users import UserProfile
from schemas.categories import GetCategory

class AssignedTask(BaseModel):
  id: str
  type: str
  title: str
  description: str
  importance: str
  completed: bool
  author: UserProfile

class GetAssignedTasks(BaseModel):
  count_of_tasks: int
  count_of_completed_tasks: int
  assigned_tasks: list[AssignedTask]

class FilterTasks(BaseModel):
  user_id: str
  is_task: bool
  is_subtask: bool
  is_completed: bool
  is_incompleted: bool
  is_very_important: str
  is_important: str
  is_low_important: str
  is_not_important: str

class CalendarAssignedTask(AssignedTask):
  category: GetCategory

class FilterCalendarTasks(FilterTasks):
  date: str