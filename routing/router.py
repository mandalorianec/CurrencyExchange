import re
from controllers.currency.currencies_controller import CurrenciesController
from controllers.currency.currency_controller import CurrencyController
from controllers.exchange.exchange_controller import ExchangeController
from controllers.exchange.exchange_rate_controller import ExchangeRateController
from controllers.exchange.exchange_rates_controller import ExchangeRatesController


class Router:
    """
    Маршрутизатор для сопоставления HTTP запросов с соответствующими контроллерами.

    Использует регулярные выражения для определения подходящего контроллера
    на основе HTTP метода и пути запроса.

    Attributes:
        _routers (list): Список кортежей (метод, regex, контроллер) для маршрутизации
    """
    _routers = [
        ("GET", r"^/currencies/?$", CurrenciesController()),
        ("GET", r"^/currency/.*$", CurrencyController()),  # любой путь после /currency/
        ("GET", r"^/exchangeRates/?$", ExchangeRatesController()),
        ("GET", r"^/exchangeRate/.*$", ExchangeRateController()),  # любой путь после /exchangeRate/
        ("GET", r"^/exchange/?.*$", ExchangeController()),  # любой путь после /exchange/
        ("POST", r"^/currencies/?$", CurrenciesController()),
        ("POST", r"^/exchangeRates/?$", ExchangeRatesController()),
        ("PATCH", r"^/exchangeRate/.*$", ExchangeRateController()),  # любой путь после /exchangeRate/
    ]

    @staticmethod
    def find_controller(method: str, path: str):
        """
        Находит подходящий контроллер для заданного метода и пути.

        Args:
            method (str): HTTP метод запроса
            path (str): Путь запроса

        Returns:
            Controller | None: Соответствующий контроллер или None если не найден

        Example:
            >>> Router.find_controller('GET', '/currency/USD')
            <CurrencyController object>
            >>> Router.find_controller('POST', '/nonexistent')
            None

        Routing Logic:
            - Проверяет совпадение метода HTTP
            - Проверяет соответствие пути регулярному выражению
            - Возвращает первый подходящий контроллер
        """
        for route_method, route, handler in Router._routers:
            if route_method == method:
                match = re.match(route, path)
                if match:
                    return handler
        return None