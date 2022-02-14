import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class ConverterFactory(ABC):
    @abstractmethod
    def get_from(self) -> str:
        pass

    @abstractmethod
    def get_to(self) -> str:
        pass


class BitcoinToDollarConverter(ConverterFactory):
    def get_from(self) -> str:
        return "BTC"

    def get_to(self) -> str:
        return "USD"


class CoinMarket(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def get_coin_info(self) -> Any:
        pass

    @abstractmethod
    def get_coin_price(self) -> float:
        pass


@dataclass
class CoinCapMarket(CoinMarket):
    factory: ConverterFactory = field(default_factory=BitcoinToDollarConverter)
    session: Session = field(init=False)
    url: str = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    api_key: str = "1d43fbc0-6c74-4bc6-ac11-15133fc660af"
    headers: Dict[Any, Any] = field(default_factory=dict, init=False)
    from_currency: str = field(init=False)
    to_currency: str = field(init=False)

    def __post_init__(self) -> None:
        # self.api_key = "1d43fbc0-6c74-4bc6-ac11-15133fc660af"
        # self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        self.headers = {
            "X-CMC_PRO_API_KEY": self.api_key,
            "Accepts": "application/json",
        }
        self.from_currency = self.factory.get_from()
        self.to_currency = self.factory.get_to()

    def connect(self) -> None:
        self.session = Session()
        self.session.headers.update(self.headers)

    def get_coin_info(self) -> Any:
        try:
            parameters = {
                "symbol": self.factory.get_from(),
                "convert": self.factory.get_to(),
            }
            response = self.session.get(self.url, params=parameters)
            data = json.loads(response.text)
            return data["data"]
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return e

    def get_coin_price(self) -> float:
        data = self.get_coin_info()
        return float(data[self.from_currency]["quote"][self.to_currency]["price"])
