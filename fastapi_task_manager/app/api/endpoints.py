import fastapi

from app.api.routers.task import router as task_router

router = fastapi.APIRouter()

router.include_router(router=task_router)
