from fastapi import APIRouter

from schemas.assigned import GetAssignedTasks, FilterTasks, CalendarAssignedTask, FilterCalendarTasks
from services.assigned import assigned_tasks_service

from utils.main import Importance

router = APIRouter()

# GET
@router.get(
  "/api/assigned/{user_id}",
  status_code=200,
  response_model=GetAssignedTasks
)
def get_assigned_tasks(user_id: str):
  return assigned_tasks_service.get_assigned_tasks(user_id)

# filter_assigned_tasks
# /{user_id}?is_task=false&is_subtask=false&is_completed=false&is_incompleted=false&is_very_important=false&is_important=false&is_low_important=false&is_not_important=false
@router.get(
  "/api/assigned/filter/{user_id}",
  status_code=200,
  response_model=GetAssignedTasks
)
def filter_assigned_tasks(
  user_id: str,
  is_task: bool = False,
  is_subtask: bool = False,
  is_completed: bool = False,
  is_incompleted: bool = False,
  is_very_important: bool = False,
  is_important: bool = False,
  is_low_important: bool = False,
  is_not_important: bool = False,
):
  is_very_import: str = Importance.very_important if is_very_important else "None"
  is_import: str = Importance.important if is_important else "None"
  is_low_import: str = Importance.low_important if is_low_important else "None"
  is_not_import: str = Importance.not_important if is_not_important else "None"
  data: FilterTasks = FilterTasks(
    user_id=user_id,
    is_task=is_task,
    is_subtask=is_subtask,
    is_completed=is_completed,
    is_incompleted=is_incompleted,
    is_very_important=is_very_import,
    is_important=is_import,
    is_low_important=is_low_import,
    is_not_important=is_not_import
  )
  return assigned_tasks_service.filter_assigned_tasks(data)

# get_calendar_dates
@router.get(
  "/api/calendar/dates/{user_id}",
  status_code=200,
  response_model=list[str]
)
def get_calendar_dates(user_id: str):
  return assigned_tasks_service.get_calendar_dates(user_id)

# get_calendar_assigned_tasks
# /{iser_id}?date=yyyy-mm-dd
@router.get(
  "/api/calendar/{user_id}",
  status_code=200,
  response_model=list[CalendarAssignedTask]
)
def get_calendar_assigned_tasks(user_id: str, date: str):
  return assigned_tasks_service.get_calendar_assigned_tasks(user_id, date)

# filter_calendar_assigned_tasks
@router.get(
  "/api/calendar/filter/{user_id}",
  status_code=200,
  response_model=list[CalendarAssignedTask]
)
def filter_calendar_assigned_tasks(
  user_id: str,
  date: str,
  is_task: bool = False,
  is_subtask: bool = False,
  is_completed: bool = False,
  is_incompleted: bool = False,
  is_very_important: bool = False,
  is_important: bool = False,
  is_low_important: bool = False,
  is_not_important: bool = False,
):
  is_very_import: str = Importance.very_important if is_very_important else "None"
  is_import: str = Importance.important if is_important else "None"
  is_low_import: str = Importance.low_important if is_low_important else "None"
  is_not_import: str = Importance.not_important if is_not_important else "None"
  data: FilterCalendarTasks = FilterCalendarTasks(
    user_id=user_id,
    is_task=is_task,
    is_subtask=is_subtask,
    is_completed=is_completed,
    is_incompleted=is_incompleted,
    is_very_important=is_very_import,
    is_important=is_import,
    is_low_important=is_low_import,
    is_not_important=is_not_import,
    date=date
  )
  return assigned_tasks_service.filter_calendar_assigned_tasks(data)