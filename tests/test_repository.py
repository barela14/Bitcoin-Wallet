import os

from app.core.repository import IRepository
from app.core.user.user import User
from app.infra.sqlite.sqlite_repository import SQLiteRepository


def reset() -> IRepository:
    os.remove("test.db")
    return SQLiteRepository("test.db")


def test_register_user() -> None:
    db = reset()
    user = User("barela", "barela_key")
    db.register_user(user)
    user_id = db.get_user_id_by_api_key("barela_key")
    assert user_id is not None and user_id == 1


def test_register_multiple_users() -> None:
    db = reset()
    for i in range(0, 10):
        user = User(str(i), str(i) + "key")
        db.register_user(user)

    for i in range(0, 10):
        user_id = db.get_user_id_by_api_key(str(i) + "key")
        assert user_id is not None and user_id == i + 1


def test_create_wallet() -> None:
    db = reset()
    user = User("tasiko", "tasikos_gasagebi")
    db.register_user(user)
    create_response = db.create_wallet("tasikos_safule", 3, "tasikos_gasagebi")
    assert create_response.status_code == 200 and create_response.args is not None


def test_create_wallets_over_limit() -> None:
    db = reset()
    user = User("tamunia", "amunia")
    db.register_user(user)
    for i in range(0, 3):
        create_response = db.create_wallet("tamunias bumajniki" + str(i), 10, "amunia")
        assert create_response.status_code == 200

    for i in range(4, 10):
        create_response = db.create_wallet("tamunias bumajniki" + str(i), 200, "amunia")
        assert create_response.status_code == 200
