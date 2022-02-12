from fastapi import FastAPI

from app.core.facade import BitcoinWalletService
from app.infra.fastapi.registration_api import registration_api
from app.infra.sqlite.sqlite_repository import SQLiteRepository


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(registration_api)
    app.state.core = BitcoinWalletService.create(repository=SQLiteRepository())

    return app
