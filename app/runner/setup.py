from fastapi import FastAPI

from app.core.facade import BitcoinWalletService
from app.infra.fastapi.admin_api import admin_api
from app.infra.fastapi.registration_api import registration_api
from app.infra.fastapi.user_api import user_api
from app.infra.sqlite.sqlite_repository import SQLiteRepository


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(registration_api)
    app.include_router(user_api)
    app.include_router(admin_api)
    app.state.core = BitcoinWalletService.create(repository=SQLiteRepository())

    return app
