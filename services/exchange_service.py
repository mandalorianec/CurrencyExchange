from decimal import Decimal, ROUND_HALF_UP

from dto.exchange_converted_dto import ExchangeConvertedDto
from dao.exchange_dao import ExchangeDao
from dao.currency_dao import CurrencyDao
from dto.exchange_convert_dto import ExchangeConvertDto
from exceptions.own_exceptions import ExchangeRateNotFoundError


class ExchangeConverter:
    """
    Сервис для конвертации валют по различным курсам обмена.

    Реализует логику поиска подходящего курса обмена в порядке приоритета:
    1. Прямой курс (базовая → целевая)
    2. Обратный курс (целевая → базовая)
    3. Через USD как валюту-посредник

    Attributes:
        _exchange_dao (ExchangeDao): DAO для работы с курсами обмена
        _currency_dao (CurrencyDao): DAO для работы с валютами
    """
    def __init__(self):
        """Инициализирует конвертер с необходимыми DAO объектами."""
        self._exchange_dao = ExchangeDao()
        self._currency_dao = CurrencyDao()

    def convert(self, exchange_dto: ExchangeConvertDto):
        """
        Конвертирует сумму из одной валюты в другую.

        Args:
            exchange_dto (ExchangeConvertDto): DTO с параметрами конвертации:
                - base (str): Код базовой валюты
                - target (str): Код целевой валюты
                - amount (Decimal): Сумма для конвертации

        Returns:
            ExchangeConvertedDto: DTO с результатом конвертации

        Raises:
            ExchangeRateNotFoundError: Если не найден подходящий курс обмена

        Conversion Logic:
            1. Пытается найти прямой курс A→B
            2. Если не найден, пытается использовать обратный курс B→A
            3. Если не найден, использует USD как посредник: A→USD→B
            4. Округляет результаты до 2 знаков после запятой

        Example:
            Конвертация 100 EUR в USD:
            - Находит курс EUR→USD = 1.05
            - Результат: 100 × 1.05 = 105.00 USD
        """
        base_currency_code = exchange_dto.base
        target_currency_code = exchange_dto.target
        amount = exchange_dto.amount
        try:
            exchange_rate_dto = self._exchange_dao.get_rate_by_codepair(base_currency_code, target_currency_code)
            rate = exchange_rate_dto.rate
            converted_amount = rate * amount
        except ExchangeRateNotFoundError:
            try:
                exchange_rate_reverse_dto = self._exchange_dao.get_rate_by_codepair(target_currency_code,
                                                                                    base_currency_code)
                rate = 1 / exchange_rate_reverse_dto.rate
                converted_amount = rate * amount
            except ExchangeRateNotFoundError:
                exchange_rate_a_dto = self._exchange_dao.get_rate_by_codepair("USD", base_currency_code)
                exchange_rate_b_dto = self._exchange_dao.get_rate_by_codepair("USD", target_currency_code)
                rate = exchange_rate_b_dto.rate / exchange_rate_a_dto.rate
                converted_amount = rate * amount
        base_currency_dto = self._currency_dao.get_currency_by_code(base_currency_code)
        target_currency_dto = self._currency_dao.get_currency_by_code(target_currency_code)
        converted_amount = converted_amount.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        rate = rate.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        exchange_converted_dto = ExchangeConvertedDto(base_currency_dto,
                                                      target_currency_dto,
                                                      rate,
                                                      amount,
                                                      converted_amount)
        return exchange_converted_dto
