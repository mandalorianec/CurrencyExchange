from decimal import Decimal, ROUND_HALF_UP

from controllers.controller import Controller
from dao.exchange_dao import ExchangeDao
from dto.exception_dto import ExceptionDTO
from dto.exchange_rate_response_dto import ExchangeRateResponseDto
from dto.response_dto import ResponseDTO
from exceptions.own_exceptions import ExchangeRateNotFoundError, DatabaseUnavailableError, \
    ExchangeRateUpdateError, InvalidCurrencyPairRequestError, MissingFormFieldError, CurrencyPairNotFoundError, \
    ValidationError
from utils.validator import Validator
from parser.code_parser import CodeParser


class ExchangeRateController(Controller):
    """
    Контроллер для операций с конкретным курсом обмена валютной пары.

    Обрабатывает запросы для получения и обновления курса обмена для конкретной пары валют.

    Attributes:
        _dao (ExchangeDao): Data Access Object для работы с курсами обмена
    """

    def __init__(self):
        """Инициализирует контроллер с DAO для работы с курсами обмена."""
        self._dao = ExchangeDao()

    def _handle_get(self, data):
        """
        Обрабатывает GET-запрос для получения курса обмена по паре валют.

        Args:
            data (dict): Данные запроса, содержащие:
                - path (str): Путь запроса с кодом пары валют (например, '/exchangeRate/USDRUB')

        Returns:
            ResponseDTO: Объект ответа с кодом статуса:
                - 200: Успешный запрос, возвращает курс обмена
                - 400: Неверный формат кода пары валют
                - 404: Курс обмена для указанной пары не найден
                - 500: Ошибка базы данных
        """
        try:
            code_pair = CodeParser.parse_code(data["path"]).upper()
            Validator.validate_pair_code(code_pair)
            base_code = code_pair[:3]
            target_code = code_pair[3:]
            rate_dto = self._dao.get_rate_by_codepair(base_code, target_code)
            response_dto = ExchangeRateResponseDto(rate_dto.id, rate_dto.base_currency, rate_dto.target_currency,
                                                   str(rate_dto.rate))
            response = ResponseDTO(200, response_dto)
        except InvalidCurrencyPairRequestError:
            response = ResponseDTO(400, ExceptionDTO(InvalidCurrencyPairRequestError()))
        except (ExchangeRateNotFoundError, CurrencyPairNotFoundError):
            response = ResponseDTO(404, ExceptionDTO(ExchangeRateNotFoundError()))
        except Exception:
            response = ResponseDTO(500, ExceptionDTO(DatabaseUnavailableError()))
            return response
        return response

    def _handle_patch(self, data):
        """
        Обрабатывает PATCH-запрос для обновления курса обмена валютной пары.

        Args:
            data (dict): Данные запроса, содержащие:
                - path (str): Путь запроса с кодом пары валют
                - body (dict): Тело запроса с параметрами:
                    - rate (str): Новое значение курса обмена

        Returns:
            ResponseDTO: Объект ответа с кодом статуса:
                - 200: Курс успешно обновлен, возвращает обновленные данные
                - 400: Ошибка валидации или отсутствуют обязательные поля
                - 404: Валютная пара не найдена
                - 500: Ошибка базы данных

        Note:
            Значение курса округляется до 2 знаков после запятой с правилом банковского округления.
        """
        path = data["path"]
        code = CodeParser.parse_code(path).upper()
        base_code = code[:3].upper()
        target_code = code[3:].upper()
        try:
            body_params = data["body"]
            Validator.validate_exchange_rate_patch(body_params)
            rate = body_params["rate"][0].replace(',', '.').replace(' ', '')
            new_rate = Decimal(rate).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
            self._dao.update_exchange_rate(base_code, target_code, new_rate)
            new_rate_dto = self._dao.get_rate_by_codepair(base_code, target_code)
            response_dto = ExchangeRateResponseDto(new_rate_dto.id, new_rate_dto.base_currency,
                                                   new_rate_dto.target_currency, str(new_rate_dto.rate))
            return ResponseDTO(200, response_dto)
        except ValidationError:
            return ResponseDTO(400, ExceptionDTO(ValidationError()))
        except MissingFormFieldError:
            return ResponseDTO(400, ExceptionDTO(MissingFormFieldError()))
        except ExchangeRateUpdateError:
            response = ResponseDTO(400, ExceptionDTO(ExchangeRateUpdateError()))
        except Exception:
            response = ResponseDTO(500, ExceptionDTO(DatabaseUnavailableError()))

        return response

    @staticmethod
    def _get_code(path) -> str:
        """
        Извлекает код валютной пары из пути запроса.

        Args:
            path (str): Путь запроса

        Returns:
            str: Код валютной пары в верхнем регистре
        """
        code = path.split("/")[-1].upper()
        return code
