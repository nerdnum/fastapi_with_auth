from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import config_manager, get_config
from app.services.database import sessionmanager


def init_app(config_file: str = 'config.json'):
    lifespan = None

    config_manager.init(config_file)
    config = get_config()

    sessionmanager.init(config['db_url'], config['config_name'])

    @ asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        if sessionmanager._engine is not None:
            await sessionmanager.close()

    server = FastAPI(title="AssumptionBook", lifespan=lifespan)
    if config['config_name'] == "testing":
        server.title = "testing"

    from app.views.auth import router as auth_router
    server.include_router(auth_router, prefix="/api", tags=["auth"])

    from app.views.users import router as user_router
    server.include_router(user_router, prefix="/api", tags=["users"])

    from app.views.roles import router as role_router
    server.include_router(role_router, prefix="/api", tags=["roles"])

    return server
