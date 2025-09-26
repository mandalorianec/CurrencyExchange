import sqlite3

from decimal import Decimal, ROUND_HALF_UP

from dto.exception_dto import ExceptionDTO
from dto.response_dto import ResponseDTO
from dto.exchange_rate_response_dto import ExchangeRateResponseDto
from controllers.controller import Controller
from dao.exchange_dao import ExchangeDao
from dao.currency_dao import CurrencyDao
from exceptions.own_exceptions import DatabaseUnavailableError, CurrencyPairAlreadyExistsError, \
    CurrencyPairNotFoundError, MissingFormFieldError, ValidationError
from utils.validator import Validator


class ExchangeRatesController(Controller):
    """
    Контроллер для операций со всеми курсами обмена.

    Обрабатывает запросы для получения списка всех курсов обмена и добавления новых курсов.
    """

    def _handle_get(self, data):
        """
        Обрабатывает GET-запрос для получения списка всех курсов обмена.

        Args:
            data (dict): Данные запроса

        Returns:
            ResponseDTO: Объект ответа с кодом статуса:
                - 200: Успешный запрос, возвращает список всех курсов обмена
                - 500: Ошибка базы данных

        Note:
            Все курсы округляются до 2 знаков после запятой с правилом банковского округления.
        """
        try:
            rates = self._get_exchange_rates()

            rates_for_response = [ExchangeRateResponseDto(rate_dto.id, rate_dto.base_currency, rate_dto.target_currency, str(rate_dto.rate.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))) for rate_dto in rates]
            response = ResponseDTO(200, rates_for_response)
        except Exception:
            response = ResponseDTO(500, ExceptionDTO(DatabaseUnavailableError()))
        return response

    def _handle_post(self, data):
        """
         Обрабатывает POST-запрос для добавления нового курса обмена.

         Args:
             data (dict): Данные запроса, содержащие:
                 - body (dict): Тело запроса с параметрами:
                     - baseCurrencyCode (str): Код базовой валюты
                     - targetCurrencyCode (str): Код целевой валюты
                     - rate (str): Значение курса обмена

         Returns:
             ResponseDTO: Объект ответа с кодом статуса:
                 - 201: Курс успешно создан, возвращает данные созданного курса
                 - 400: Ошибка валидации или отсутствуют обязательные поля
                 - 404: Одна или обе валюты не найдены
                 - 409: Курс обмена для указанной пары уже существует
                 - 500: Ошибка базы данных

         Note:
             Значение курса округляется до 2 знаков после запятой с правилом банковского округления.
         """
        _currency_dao = CurrencyDao()
        _exchange_dao = ExchangeDao()
        rates_data = data["body"]
        try:
            Validator.validate_exchange_rates_post(rates_data)

            base_currency_code = rates_data["baseCurrencyCode"][0].upper()
            target_currency_code = rates_data["targetCurrencyCode"][0].upper()
            rate = Decimal(rates_data["rate"][0]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

            cur_dto = _currency_dao.get_currency_pair_id(base_currency_code, target_currency_code)
            _exchange_dao.add_new_exchange_rate(cur_dto.base_currency_id, cur_dto.target_currency_id, rate)
            exchange_dto = _exchange_dao.get_rate_by_codepair(base_currency_code, target_currency_code)
            response_dto = ExchangeRateResponseDto(exchange_dto.id, exchange_dto.base_currency, exchange_dto.target_currency, str(exchange_dto.rate))

            response = ResponseDTO(201, response_dto)
        except ValidationError:
            return ResponseDTO(400, ExceptionDTO(ValidationError()))
        except MissingFormFieldError:
            return ResponseDTO(400, ExceptionDTO(MissingFormFieldError()))
        except sqlite3.IntegrityError:
            response = ResponseDTO(409, ExceptionDTO(CurrencyPairAlreadyExistsError()))
        except CurrencyPairNotFoundError:
            response = ResponseDTO(404, ExceptionDTO(CurrencyPairNotFoundError))
        except Exception:
            response = ResponseDTO(500, ExceptionDTO(DatabaseUnavailableError()))
        return response

    @staticmethod
    def _get_exchange_rates():
        """
        Получает все курсы обмена из базы данных.

        Returns:
            list: Список DTO объектов курсов обмена

        Raises:
            Exception: Если произошла ошибка при работе с базой данных
        """
        dao = ExchangeDao()
        ex_rates = dao.read_all()
        return ex_rates
