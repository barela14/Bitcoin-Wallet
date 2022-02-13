from dataclasses import dataclass

from app.core.admin.interactor import AdminInteractor
from app.core.registration.interactor import RegistrationInteractor
from app.core.repository import IRepository
from app.core.user.interactor import UserInteractor
from app.infra.fastapi.responses import (
    CreateWalletResponseWrapper,
    RegistrationResponse,
    Response,
    GetWalletResponseWrapper,
    GetTransactionResponse, GetStatisticsResponse,
)


@dataclass
class BitcoinWalletService:
    register_interactor: RegistrationInteractor
    user_interactor: UserInteractor
    admin_interactor: AdminInteractor

    def register_user(self, user_name: str) -> RegistrationResponse:
        return self.register_interactor.register_user(user_name)

    def create_wallet(self, api_key: str) -> CreateWalletResponseWrapper:
        return self.user_interactor.create_wallet(api_key)

    def get_wallet(self, api_key: str, address: str) -> GetWalletResponseWrapper:
        return self.user_interactor.get_wallet(api_key, address)

    def make_transaction(
        self, api_key: str, address_from: str, address_to: str, amount: float
    ) -> Response:
        return self.user_interactor.make_transaction(
            api_key, address_from, address_to, amount
        )

    def get_transactions(self, api_key: str) -> GetTransactionResponse:
        return self.user_interactor.get_transactions(api_key)

    def get_wallet_transactions(
        self, api_key: str, address: str
    ) -> GetTransactionResponse:
        return self.user_interactor.get_wallet_transactions(api_key, address)

    def get_statistics(self, admin_api_key: str) -> GetStatisticsResponse:
        return self.admin_interactor.get_statistics(admin_api_key)

    @classmethod
    def create(cls, repository: IRepository) -> "BitcoinWalletService":
        return cls(
            register_interactor=RegistrationInteractor(repository),
            user_interactor=UserInteractor(repository),
            admin_interactor=AdminInteractor(repository)
        )

