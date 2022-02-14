import os

from app.core.facade import BitcoinWalletService
from app.infra.sqlite.sqlite_repository import SQLiteRepository

admin_key = "ken-cho"


def reset() -> BitcoinWalletService:
    os.remove("test.db")
    return BitcoinWalletService.create(repository=SQLiteRepository("test.db"))


def test_nothing() -> None:
    assert True


def test_admin_wrong_key() -> None:
    service = reset()
    response = service.admin_interactor.get_statistics("wrong key")
    assert response.status_code == 1 and response.status_message == "Invalid admin key"


def test_admin_valid_key() -> None:
    service = reset()
    response = service.get_statistics(admin_key)
    assert response.status_code == 200 and response.status_message == "OK"


def test_create_wallet_wrong_key() -> None:
    service = reset()
    response = service.create_wallet("non-existent-key")
    assert response.status_code != 200 and response.status_message != "OK"


def test_create_wallet_valid_key() -> None:
    service = reset()
    user_key = service.register_user("barela").api_key
    response = service.create_wallet(user_key)
    assert response.status_code == 200 and response.status_message == "OK"


def test_get_wallet_valid_address() -> None:
    service = reset()
    user_key = service.register_user("barela").api_key
    wallet = service.create_wallet(user_key).args
    assert wallet is not None
    address = wallet.address
    response = service.get_wallet(user_key, address)
    assert response is not None and response.args is not None
    assert response.status_code == 200 and response.args.balance_bitcoin == 1


def test_get_wallet_wrong_address() -> None:
    service = reset()
    wallet = service.create_wallet("very invalid address").args
    assert wallet is None


def test_get_profits_no_transactions() -> None:
    service = reset()
    response = service.get_statistics(admin_key)
    assert response.total_profit == 0


def test_get_profits_self_transaction() -> None:
    service = reset()
    user = service.register_user("user_name")
    api_key = user.api_key
    wallet_one = service.create_wallet(api_key).args
    wallet_two = service.create_wallet(api_key).args
    assert wallet_one is not None
    assert wallet_two is not None
    transaction_response = service.make_transaction(
        api_key, wallet_one.address, wallet_two.address, 1.0
    )
    assert (
        transaction_response.status_code == 200
        and transaction_response.status_message == "OK"
    )

    profit = service.get_statistics(admin_key).total_profit
    assert profit == 0


def test_get_profits_foreign_transaction() -> None:
    service = reset()
    key_one = service.register_user("one").api_key
    key_two = service.register_user("two").api_key
    wallet_one = service.create_wallet(key_one).args
    wallet_two = service.create_wallet(key_two).args
    assert wallet_one is not None
    assert wallet_two is not None
    transaction_response = service.make_transaction(
        key_one, wallet_one.address, wallet_two.address, 1.0
    )
    assert (
        transaction_response.status_code == 200
        and transaction_response.status_message == "OK"
    )

    profit = service.get_statistics(admin_key).total_profit
    assert profit == 0.15


def test_number_of_transactions() -> None:
    service = reset()
    key_one = service.register_user("one").api_key
    key_two = service.register_user("two").api_key
    wallet_one = service.create_wallet(key_one).args
    wallet_two = service.create_wallet(key_two).args
    assert wallet_one is not None
    assert wallet_two is not None
    for i in range(0, 10):
        service.make_transaction(key_one, wallet_one.address, wallet_two.address, 0.1)
    num_transactions = service.get_statistics(admin_key).num_transactions
    assert num_transactions == 10
