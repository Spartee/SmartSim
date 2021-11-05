from fastapi import APIRouter

from .routers import experiment, model, execute

router = APIRouter()
router.include_router(experiment.router, tags=["experiment"], prefix="/experiment")
router.include_router(model.router, tags=["model"], prefix="/model")
router.include_router(execute.router, tags=["execute"], prefix="/execute")
