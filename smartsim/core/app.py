from fastapi import FastAPI
from starlette.requests import Request

#from .taskManager import TaskManager
#from .jobmonitor import JobMonitor
from .common import constants
from .backend.db.session import Session, DBBase, engine
from .backend.routes import router as api_router

import threading

DBBase.metadata.create_all(bind=engine)

def get_application() -> FastAPI:
    application = FastAPI(
        title=constants.PROJECT_NAME,
        debug=constants.DEBUG,
        version=constants.VERSION,
        docs_url="/docs"
    )
    application.include_router(
        api_router, prefix=constants.API_PREFIX,
    )
    return application


app = get_application()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


# Application lock
#lock = threading.Rlock()

# task manager
#task_manager = TaskManager(lock)

# job manager
#job_manager = JobMonitor()