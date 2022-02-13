import random
import string
from dataclasses import dataclass
from typing import Callable, Set

from app.core.repository import IRepository
from app.core.user.user import Transaction
from app.infra.fastapi.responses import (
    BitcoinWalletWrapper,
    CreateWalletResponseWrapper,
    GetWalletResponseWrapper,
    Response,
    GetTransactionResponse,
)


def simple_address_generator(arg: str) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


@dataclass
class UserInteractor:
    repository: IRepository
    starting_deposit: float = 1.0
    address_fn: Callable[[str], str] = simple_address_generator

    def create_wallet(self, api_key: str) -> CreateWalletResponseWrapper:
        user_id = self.repository.get_user_id_by_api_key(api_key)
        if user_id is None:
            return CreateWalletResponseWrapper(1, "Wrong api_key")
        wallets = self.repository.get_wallets_by_user_id(user_id)
        if len(wallets) >= 3:
            return CreateWalletResponseWrapper(1, "Can't add any more wallets")

        address = self.address_fn("")
        wallet_result = self.repository.create_wallet(address, 1.0, api_key)

        args = wallet_result.args
        assert args is not None
        new_args = BitcoinWalletWrapper(args.address, args.balance, 7)
        return CreateWalletResponseWrapper(
            wallet_result.status_code, wallet_result.status_message, new_args
        )

    def get_wallet(self, api_key: str, address: str) -> GetWalletResponseWrapper:
        user_id = self.repository.get_user_id_by_api_key(api_key)
        if user_id is None:
            return GetWalletResponseWrapper(1, "Wrong api_key")

        wallet_result = self.repository.get_wallet_by_address(address)
        args = wallet_result.args
        if args is None:
            return GetWalletResponseWrapper(
                wallet_result.status_code, wallet_result.status_message
            )

        assert args is not None
        new_args = BitcoinWalletWrapper(args.address, args.balance, 8)
        return GetWalletResponseWrapper(
            wallet_result.status_code, wallet_result.status_message, new_args
        )

    def make_transaction(
        self, api_key: str, address_from: str, address_to: str, amount: float
    ) -> Response:
        user_id = self.repository.get_user_id_by_api_key(api_key)
        if user_id is None:
            return Response(1, "Wrong api_key")

        wallet_from = self.repository.get_wallet_by_address(address_from)
        if wallet_from.args is None:
            return Response(
                wallet_from.status_code, "Address not found in your wallets"
            )
        assert wallet_from is not None
        wallets = self.repository.get_wallets_by_user_id(user_id)

        wallet_to = self.repository.get_wallet_by_address(address_to)
        args_to = wallet_to.args
        if args_to is None:
            return Response(wallet_to.status_code, "Couldn't find second wallet")

        user_to_id = self.repository.get_user_id_by_wallet_address(address_to)
        assert user_to_id is not None
        assert args_to is not None
        if args_to in wallets:
            return self.transaction(
                address_from, address_to, amount, user_id, user_to_id
            )

        return self.transaction(address_from, address_to, amount, user_id, user_to_id)

    def transaction(
        self,
        address_from: str,
        address_to: str,
        amount: float,
        user_from_id: int,
        user_to_id: int,
    ) -> Response:

        modifier = 1.0 if user_from_id == user_to_id else 0.85

        update_from = self.repository.update_wallet_balance(address_from, -amount)
        if update_from.status_code != 200:
            return update_from

        update_to = self.repository.update_wallet_balance(address_to, amount * modifier)
        if update_to.status_code != 200:
            update_revert_transaction = self.repository.update_wallet_balance(
                address_from, amount
            )
            while update_revert_transaction.status_code != 200:
                update_revert_transaction = self.repository.update_wallet_balance(
                    address_from, amount
                )
            return update_to
        return self.repository.register_transaction(
            address_from, address_to, amount, user_from_id, user_to_id
        )

    def get_transactions(self, api_key: str) -> GetTransactionResponse:
        user_id = self.repository.get_user_id_by_api_key(api_key)
        if user_id is None:
            return GetTransactionResponse(1, "Wrong api_key")

        wallets = self.repository.get_wallets_by_user_id(user_id)
        transactions: Set[Transaction] = set()
        for wallet in wallets:
            wallet_transaction = self.get_wallet_transactions(
                api_key, wallet.address
            ).args
            if wallet_transaction is not None:
                transactions = transactions.union(wallet_transaction)
        return GetTransactionResponse(200, "OK", list(transactions))

    def get_wallet_transactions(
        self, api_key: str, address: str
    ) -> GetTransactionResponse:
        user_id = self.repository.get_user_id_by_api_key(api_key)
        if user_id is None:
            return GetTransactionResponse(1, "Wrong api_key")
        wallet = self.repository.get_wallet_by_address(address)
        if wallet.args is None:
            return GetTransactionResponse(
                wallet.status_code, "Address not found in your wallets"
            )
        assert wallet is not None
        return GetTransactionResponse(
            200, "OK", self.repository.get_wallet_transactions_by_address(address)
        )
