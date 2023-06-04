from fastapi import APIRouter

from api.users import router as users_router
from api.categories import router as categories_router
from api.colors import router as colors_router
from api.projects import router as projects_router
from api.tasks import router as tasks_router
from api.subtasks import router as subtasks_router
from api.assigned import router as assigned_router

router = APIRouter()

router.include_router(users_router)
router.include_router(colors_router)
router.include_router(categories_router)
router.include_router(projects_router)
router.include_router(tasks_router)
router.include_router(subtasks_router)
router.include_router(assigned_router)