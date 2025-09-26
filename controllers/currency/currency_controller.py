from parser.code_parser import CodeParser
from controllers.controller import Controller
from dao.currency_dao import CurrencyDao
from dto.exception_dto import ExceptionDTO
from dto.response_dto import ResponseDTO
from exceptions.own_exceptions import CurrencyNotFoundError, DatabaseUnavailableError, InvalidCurrencyRequestError
from utils.validator import Validator


class CurrencyController(Controller):
    """
    Контроллер для операций с конкретной валютой по коду.

    Обрабатывает запросы для получения информации о конкретной валюте.

    Attributes:
        _dao (CurrencyDao): Data Access Object для работы с данными валют
    """
    def __init__(self):
        """Инициализирует контроллер с DAO для работы с валютами."""
        self._dao = CurrencyDao()

    def _handle_get(self, data):
        """
        Обрабатывает GET-запрос для получения информации о конкретной валюте.

        Извлекает код валюты из пути запроса, валидирует его и возвращает данные валюты.

        Args:
            data (dict): Данные запроса, содержащие:
                - path (str): Путь запроса с кодом валюты (например, '/currency/USD')

        Returns:
            ResponseDTO: Объект ответа с кодом статуса:
                - 200: Успешный запрос, возвращает данные валюты
                - 400: Неверный формат запроса или кода валюты
                - 404: Валюта с указанным кодом не найдена
                - 500: Ошибка базы данных
        """
        try:
            path = data["path"]
            code = CodeParser.parse_code(path).upper()
            Validator.validate_currency_controller(code)
            currency = self._dao.get_currency_by_code(code)
        except InvalidCurrencyRequestError:
            return ResponseDTO(400, ExceptionDTO(InvalidCurrencyRequestError()))
        except CurrencyNotFoundError:
            return ResponseDTO(404, ExceptionDTO(CurrencyNotFoundError()))
        except Exception:
            return ResponseDTO(500, ExceptionDTO(DatabaseUnavailableError()))
        response = ResponseDTO(200, currency)
        return response
