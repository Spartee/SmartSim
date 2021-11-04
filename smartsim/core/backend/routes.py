from fastapi import APIRouter

from .routers import experiment, model

router = APIRouter()
router.include_router(experiment.router, tags=["experiment"], prefix="/experiment")
router.include_router(model.router, tags=["model"], prefix="/model")
