from fastapi import APIRouter

from services.tasks.router import router as tasks_router
from services.trello.router import router as trello_router
from services.users.router import router as users_router

router = APIRouter(prefix="/api/v1")


router.include_router(users_router, prefix="/users")
router.include_router(tasks_router, prefix="/tasks")
router.include_router(trello_router, prefix="/trello")
