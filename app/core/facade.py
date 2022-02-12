from dataclasses import dataclass

from app.core.registration.interactor import RegistrationInteractor
from app.core.repository import IRepository
from app.infra.fastapi.responses import RegistrationResponse


@dataclass
class BitcoinWalletService:
    register_interactor: RegistrationInteractor

    def register_user(self) -> RegistrationResponse:
        return self.register_interactor.register_user()

    @classmethod
    def create(cls, repository: IRepository) -> "BitcoinWalletService":
        return cls(
            register_interactor=RegistrationInteractor(repository),
        )
