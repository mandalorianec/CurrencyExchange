from exceptions.own_exceptions import InvalidCurrencyRequestError, InvalidCurrencyPairRequestError, \
    MissingFormFieldError, ValidationError
import re
import math


class Validator:
    """
    Класс для валидации различных типов данных в приложении.

    Содержит статические методы для проверки корректности:
    - Кодов валют
    - Данных форм
    - Числовых значений
    - Пар валют

    Methods:
        validate_currency_controller: Валидация кода валюты
        validate_post_currencies_controller: Валидация данных новой валюты
        validate_pair_code: Валидация кода пары валют
        validate_exchange_rates_post: Валидация данных нового курса обмена
        validate_exchange_rate_patch: Валидация данных обновления курса
        validate_exchange: Валидация суммы для конвертации
        _validate_number: Внутренняя валидация числовых значений
    """

    @staticmethod
    def validate_currency_controller(code: str):
        """
         Валидирует код валюты для контроллера.

         Args:
             code (str): Код валюты для проверки

         Raises:
             InvalidCurrencyRequestError: Если код пустой
             ValidationError: Если код не 3 буквы или содержит не-буквенные символы
         """
        code = code.strip().upper()
        if len(code) == 0:
            raise InvalidCurrencyRequestError
        if len(code) != 3 or not code.isalpha():
            raise ValidationError

    @staticmethod
    def validate_post_currencies_controller(code: str, name: str, sign: str):
        """
         Валидирует данные для создания новой валюты.

         Args:
             code (str): Код валюты (3 буквы)
             name (str): Название валюты (до 30 символов, буквы и пробелы)
             sign (str): Символ валюты (до 10 символов)

         Raises:
             InvalidCurrencyRequestError: Если любое поле пустое
             ValidationError: Если данные не соответствуют формату
         """
        if not code or not name or not sign:
            raise InvalidCurrencyRequestError
        if len(code) != 3 or not code.isalpha() or not re.fullmatch(r"[A-Za-z ]+", name) or len(name) > 30 or len(
                sign) > 10:
            raise ValidationError

    @staticmethod
    def validate_pair_code(code: str):
        """
        Валидирует код пары валют.

        Args:
            code (str): Код пары валют (например, 'USDRUB')

        Raises:
            InvalidCurrencyPairRequestError: Если код пустой
        """
        if len(code) == 0:
            raise InvalidCurrencyPairRequestError

    @staticmethod
    def validate_exchange_rates_post(params: dict):
        """
         Валидирует данные для создания нового курса обмена.

         Args:
             params (dict): Параметры запроса с полями:
                 - baseCurrencyCode (str): Код базовой валюты
                 - targetCurrencyCode (str): Код целевой валюты
                 - rate (str): Значение курса

         Raises:
             MissingFormFieldError: Если отсутствуют обязательные поля
             ValidationError: Если валидация не пройдена
         """
        fields = ["baseCurrencyCode", "targetCurrencyCode", "rate"]
        # проверка на пустую форму
        for field in fields:
            if field not in params:
                raise MissingFormFieldError
            if not params[field] or len(params[field]) == 0:
                raise MissingFormFieldError
        # нельзя сделать курс валюты к самой себе
        if params["baseCurrencyCode"][0].upper() == params["targetCurrencyCode"][0].upper():
            raise ValidationError
        rate = params["rate"][0].replace(',', '.').replace(' ', '')
        # проверка rate
        Validator._validate_number(rate)

    @staticmethod
    def validate_exchange_rate_patch(params: dict):
        """
         Валидирует данные для обновления курса обмена.

         Args:
             params (dict): Параметры запроса с полем 'rate'

         Raises:
             MissingFormFieldError: Если поле rate отсутствует или пустое
             ValidationError: Если значение rate невалидно
         """
        if "rate" not in params:
            raise MissingFormFieldError
        if len(params["rate"]) == 0:
            raise MissingFormFieldError
        rate = params["rate"][0].replace(',', '.').replace(' ', '')
        Validator._validate_number(rate)

    @staticmethod
    def validate_exchange(amount):
        """
        Валидирует сумму для конвертации валют.

        Args:
            amount (str): Сумма для конвертации

        Raises:
            ValidationError: Если сумма невалидна
        """
        amount = amount.replace(',', '.').replace(' ', '')
        Validator._validate_number(amount)

    @staticmethod
    def _validate_number(rate):
        """
        Внутренний метод для валидации числовых значений.

        Args:
            rate (str): Числовое значение в виде строки

        Raises:
            ValidationError: Если значение не является положительным числом

        Validation Rules:
            - Не пустая строка
            - Не содержит букв
            - Максимум одна десятичная точка
            - Не NaN
            - Положительное число > 0.01
        """
        if len(rate) == 0:
            raise ValidationError
        if rate.isalpha():
            raise ValidationError
        if rate.count('.') > 1:
            raise ValidationError
        try:
            tmp = float(rate)
        except Exception:
            raise ValidationError
        if math.isnan(float(rate)):
            raise ValidationError
        if float(rate) <= 0:
            raise ValidationError
        if float(rate) < 0.01:
            raise ValidationError
