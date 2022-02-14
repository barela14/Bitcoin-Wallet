import os
from typing import Tuple

from app.core.facade import BitcoinWalletService
from app.core.user.interactor import UserInteractor
from app.infra.sqlite.sqlite_repository import SQLiteRepository


def reset() -> Tuple[str, UserInteractor]:
    os.remove("test.db")
    service = BitcoinWalletService.create(repository=SQLiteRepository("test.db"))
    user_key = service.register_user("barela").api_key
    return user_key, UserInteractor(repository=SQLiteRepository("test.db"))


def test_create_wallet_wrong_key() -> None:
    user_key, interactor = reset()
    response = interactor.create_wallet("non-existent-key")
    assert response.status_code != 200 and response.status_message != "OK"


def test_create_wallet_valid_key() -> None:
    user_key, interactor = reset()
    response = interactor.create_wallet(user_key)
    assert response.status_code == 200 and response.status_message == "OK"


def test_get_wallet_valid_address() -> None:
    user_key, interactor = reset()
    wallet = interactor.create_wallet(user_key).args
    assert wallet is not None
    address = wallet.address
    response = interactor.get_wallet(user_key, address)
    assert response is not None and response.args is not None
    assert response.status_code == 200 and response.args.balance_bitcoin == 1


def test_get_wallet_wrong_address() -> None:
    user_key, interactor = reset()
    wallet = interactor.create_wallet("very invalid address").args
    assert wallet is None


def test_create_wallets_over_limit() -> None:
    user_key, interactor = reset()
    for i in range(0, 3):
        create_response = interactor.create_wallet(user_key)
        assert create_response.status_code == 200

    for i in range(4, 10):
        create_response = interactor.create_wallet(user_key)
        assert create_response.status_code == 1
