import random
import string
from dataclasses import dataclass
from typing import Callable

from app.core.repository import IRepository
from app.core.user.user import User
from app.infra.fastapi.responses import RegistrationResponse


def simple_key_generator(arg: str) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


@dataclass
class RegistrationInteractor:
    repository: IRepository
    api_key_fn: Callable[[str], str] = simple_key_generator

    def set_api_key_function(self, new_func: Callable[[str], str]) -> None:
        self.api_key_fn = new_func

    def register_user(self, user_name: str) -> RegistrationResponse:
        api_key = self.api_key_fn("ragaca")
        user = User(user_name, api_key)
        self.repository.register_user(user)
        return RegistrationResponse(user_name, api_key)
