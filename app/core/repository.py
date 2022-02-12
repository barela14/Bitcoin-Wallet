from typing import Protocol


class IRepository(Protocol):
    def register_user(self, api_key: str) -> None:
        pass
