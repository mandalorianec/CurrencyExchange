from decimal import Decimal, ROUND_HALF_UP

from dto.exception_dto import ExceptionDTO
from dto.exchange_convert_dto import ExchangeConvertDto
from controllers.controller import Controller
from exceptions.own_exceptions import ExchangeRateNotFoundError, DatabaseUnavailableError, ValidationError
from services.exchange_service import ExchangeConverter
from dto.response_dto import ResponseDTO
from dto.exchange_converted_response_dto import ExchangeConvertedResponseDto
from utils.validator import Validator


class ExchangeController(Controller):
    """
    Контроллер для конвертации суммы из одной валюты в другую.

    Обрабатывает запросы на конвертацию валют с использованием актуальных курсов.

    Attributes:
        _converter (ExchangeConverter): Сервис для выполнения конвертации валют
    """

    def __init__(self):
        """Инициализирует контроллер с сервисом конвертации валют."""
        self._converter = ExchangeConverter()

    def _handle_get(self, data):
        """
        Обрабатывает GET-запрос для конвертации суммы между валютами.

        Args:
            data (dict): Данные запроса, содержащие:
                - query_params (dict): Параметры строки запроса:
                    - from (str): Код базовой валюты
                    - to (str): Код целевой валюты
                    - amount (str): Сумма для конвертации

        Returns:
            ResponseDTO: Объект ответа с кодом статуса:
                - 200: Успешная конвертация, возвращает результат
                - 400: Ошибка валидации параметров
                - 404: Обменный курс для указанной пары не найден
                - 500: Ошибка базы данных

        Note:
            Все числовые значения округляются до 2 знаков после запятой с правилом банковского округления.
        """
        query_params = data["query_params"]
        base = query_params["from"][0]
        target = query_params["to"][0]
        amount = query_params["amount"][0]
        try:
            Validator.validate_exchange(amount)
            amount = Decimal(query_params["amount"][0]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
            to_convert_dto = ExchangeConvertDto(base, target, amount)
            converted_dto = self._converter.convert(to_convert_dto)
            rate_response = str(converted_dto.rate.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
            amount_response = str(converted_dto.amount.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
            converted_amount_reponse = str(
                converted_dto.converted_amount.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
            converted_dto_response = ExchangeConvertedResponseDto(converted_dto.base, converted_dto.target,
                                                                  rate_response, amount_response,
                                                                  converted_amount_reponse)
        except ValidationError:
            return ResponseDTO(400, ExceptionDTO(ValidationError()))
        except ExchangeRateNotFoundError:
            return ResponseDTO(404, ExceptionDTO(ExchangeRateNotFoundError()))
        except Exception:
            return ResponseDTO(500, ExceptionDTO(DatabaseUnavailableError()))
        return ResponseDTO(200, converted_dto_response)
