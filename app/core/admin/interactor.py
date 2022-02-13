from dataclasses import dataclass

from app.core.repository import IRepository
from app.infra.fastapi.responses import GetStatisticsResponse


def validate_admin_key(admin_api_key: str) -> bool:
    return admin_api_key == "ken-cho"


@dataclass
class AdminInteractor:
    repository: IRepository

    def get_statistics(self, admin_api_key: str) -> GetStatisticsResponse:
        if not validate_admin_key(admin_api_key):
            return GetStatisticsResponse(1, "Invalid admin key")
        num_transactions = self.repository.get_number_of_transactions()
        profit = self.repository.get_foreign_transactions_amount() * 0.15
        return GetStatisticsResponse(200, "OK", num_transactions, profit)
