from fastapi import HTTPException

from schemas.assigned import FilterTasks, GetAssignedTasks, AssignedTask, CalendarAssignedTask, FilterCalendarTasks
from schemas.users import UserProfile
from schemas.tasks import Task
from schemas.subtasks import Subtask
from schemas.categories import GetCategory

from db.users import find_user
from db.tasks import filter_tasks
from db.subtasks import filter_subtasks

from services.users import users_service
from services.categories import categories_service

from utils.main import calculate_importance, convert_date_to_ms, Importance, convert_ms_to_simple_date

class AssignedTasksService:
  # get_assigned_tasks
  def get_assigned_tasks(self, user_id) -> GetAssignedTasks:
    return self.filter_assigned_tasks(FilterTasks(
      user_id=user_id,
      is_task=True,
      is_subtask=True,
      is_completed=True,
      is_incompleted=True,
      is_very_important=Importance.very_important,
      is_important=Importance.important,
      is_low_important=Importance.low_important,
      is_not_important=Importance.not_important
    ))

  # filter_assigned_tasks
  def filter_assigned_tasks(self, data: FilterTasks) -> GetAssignedTasks:
    if find_user(data.user_id) == None:
      raise HTTPException(status_code=404, detail="Пользователь не найден!")
    assigned_tasks: list[AssignedTask] = []

    tasks: list[Task] = filter_tasks(data.user_id)
    subtasks: list[Subtask] = filter_subtasks(data.user_id)

    count_of_tasks = len(tasks) + len(subtasks)
    count_of_completed_tasks = 0

    for task in tasks:
      if task.completed == True: count_of_completed_tasks += 1

      if self._filter_condition(task=task, is_task=data.is_task, data=data):
        importance: str = task.importance
        if len(importance) == 0:
          importance = calculate_importance(task.deadline)
        author: UserProfile = users_service.get_user(task.author_id)
        assigned_task: AssignedTask = AssignedTask(id=task.id, type="task", title=task.title, description=task.description, importance=importance, author=author, completed=task.completed)
        assigned_tasks.append(assigned_task)

    for subtask in subtasks:
      if subtask.completed == True: count_of_completed_tasks += 1

      if self._filter_condition(task=subtask, is_task=data.is_subtask, data=data):
        importance: str = subtask.importance
        if len(importance) == 0:
          importance = calculate_importance(subtask.deadline)
        author: UserProfile = users_service.get_user(subtask.author_id)
        assigned_subtask: AssignedTask = AssignedTask(id=subtask.id, type="subtask", title=subtask.title, description=subtask.description, importance=importance, author=author, completed=subtask.completed)
        assigned_tasks.append(assigned_subtask)

    return GetAssignedTasks(
      count_of_tasks=count_of_tasks,
      count_of_completed_tasks=count_of_completed_tasks,
      assigned_tasks=assigned_tasks
    )

  def get_calendar_dates(self, user_id: str) -> list[str]:
    if find_user(user_id) == None:
      raise HTTPException(status_code=404, detail="Пользователь не найден!")

    dates: list[str] = []

    tasks: list[Task] = filter_tasks(user_id)
    subtasks: list[Subtask] = filter_subtasks(user_id)

    for task in tasks:
      isNext: bool = False
      for date in dates:
        if convert_ms_to_simple_date(task.deadline) == date: isNext = True; break
      if isNext == False: dates.append(convert_ms_to_simple_date(task.deadline))

    for subtask in subtasks:
      isNext: bool = False
      for date in dates:
        if convert_ms_to_simple_date(subtask.deadline) == date: isNext = True; break
      if isNext == False: dates.append(convert_ms_to_simple_date(subtask.deadline))
    
    return dates


  # get_calendar_assigned_tasks
  def get_calendar_assigned_tasks(self, user_id: str, date: str) -> list[CalendarAssignedTask]:
    return self.filter_calendar_assigned_tasks(FilterCalendarTasks(
      user_id=user_id,
      is_task=True,
      is_subtask=True,
      is_completed=True,
      is_incompleted=True,
      is_very_important=Importance.very_important,
      is_important=Importance.important,
      is_low_important=Importance.low_important,
      is_not_important=Importance.not_important,
      date=date
    ))

  # filter_calendar_assigned_tasks
  def filter_calendar_assigned_tasks(self, data: FilterCalendarTasks) -> list[CalendarAssignedTask]:
    if find_user(data.user_id) == None:
      raise HTTPException(status_code=404, detail="Пользователь не найден!")
    calendar_assigned_tasks: list[CalendarAssignedTask] = []

    tasks: list[Task] = filter_tasks(data.user_id)
    subtasks: list[Subtask] = filter_subtasks(data.user_id)

    for task in tasks:
      if self._filter_condition(task=task, is_task=data.is_task, data=data, date=data.date):
        importance: str = task.importance
        if len(importance) == 0:
          importance = calculate_importance(task.deadline)
        author: UserProfile = users_service.get_user(task.author_id)
        category: GetCategory = categories_service.get_category(task.category_id)
        calendar_assigned_task: CalendarAssignedTask = CalendarAssignedTask(id=task.id, type="Задача", title=task.title, description=task.description, importance=importance, author=author, completed=task.completed, category=category)
        calendar_assigned_tasks.append(calendar_assigned_task)

    for subtask in subtasks:
      if self._filter_condition(task=subtask, is_task=data.is_subtask, data=data, date=data.date):
        importance: str = subtask.importance
        if len(importance) == 0:
          importance = calculate_importance(subtask.deadline)
        author: UserProfile = users_service.get_user(subtask.author_id)
        category: GetCategory = categories_service.get_category(subtask.category_id)
        calendar_assigned_subtask: CalendarAssignedTask = CalendarAssignedTask(id=subtask.id, type="Подзадача", title=subtask.title, description=subtask.description, importance=importance, author=author, completed=subtask.completed, category=category)
        calendar_assigned_tasks.append(calendar_assigned_subtask)

    return calendar_assigned_tasks

  # _filter_condition
  def _filter_condition(self, task, is_task: bool, data, date: str = "") -> bool:
    if((date == "" or convert_date_to_ms(date) == task.deadline) and (is_task or data.is_task == data.is_subtask) and (data.is_completed == data.is_incompleted or task.completed == data.is_completed or task.completed != data.is_incompleted) and
        (
          (data.is_very_important == "None" and data.is_important == "None" and data.is_low_important == "None" and data.is_not_important == "None") or
          task.importance == data.is_very_important or task.importance == data.is_important or
          task.importance == data.is_low_important or task.importance == data.is_not_important or
          (len(task.importance) == 0 and (
            calculate_importance(task.deadline) == data.is_very_important or calculate_importance(task.deadline) == data.is_important or
            calculate_importance(task.deadline) == data.is_low_important or calculate_importance(task.deadline) == data.is_not_important
            )
          )
        )
      ): return True
    return False

assigned_tasks_service: AssignedTasksService = AssignedTasksService()