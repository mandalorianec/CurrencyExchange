import sqlite3

from dao.currency_dao import CurrencyDao
from controllers.controller import Controller
from dto.response_dto import ResponseDTO
from dto.exception_dto import ExceptionDTO
from exceptions.own_exceptions import DatabaseUnavailableError, CurrencyAlreadyExistsError, MissingFormFieldError, \
    ValidationError, InvalidCurrencyRequestError
from utils.validator import Validator
from urllib.parse import unquote_plus


class CurrenciesController(Controller):
    """
    Контроллер для управления валютами.

    Обрабатывает HTTP-запросы, связанные с операциями над валютами:
    - Получение списка всех валют
    - Добавление новой валюты
    """

    def __init__(self):
        """Инициализирует контроллер с DAO для работы с валютами."""
        self._dao = CurrencyDao()

    def _handle_get(self, data):
        """
        Обрабатывает GET-запрос для получения списка всех валют.

        Args:
            data (dict): Данные запроса (не используются в этом методе)

        Returns:
            ResponseDTO: Объект ответа с кодом статуса и данными:
                - 200: Успешный запрос, возвращает список валют
                - 500: Ошибка базы данных
        """
        try:
            currencies_dto = self._dao.get_currencies()
            response = ResponseDTO(200, currencies_dto)
        except Exception:
            response = ResponseDTO(500, ExceptionDTO(DatabaseUnavailableError()))
        return response

    def _handle_post(self, data):
        """
        Обрабатывает POST-запрос для добавления новой валюты.

        Args:
            data (dict): Данные запроса, содержащие:
                - body (dict): Тело запроса с параметрами валюты:
                    - code (str): Код валюты (например, 'USD')
                    - name (str): Название валюты
                    - sign (str): Символ валюты (например, '$')

        Returns:
            ResponseDTO: Объект ответа с кодом статуса:
                - 201: Валюта успешно создана, возвращает данные созданной валюты
                - 400: Ошибка валидации или отсутствуют обязательные поля
                - 409: Валюта с таким кодом уже существует
                - 500: Ошибка базы данных

        Raises:
            ValidationError: Если данные не прошли валидацию
            KeyError, IndexError: Если отсутствуют обязательные поля
            sqlite3.IntegrityError: Если валюта с таким кодом уже существует
        """
        currency_data = data["body"]
        try:

            code = unquote_plus(currency_data["code"][0]).strip().upper()
            name = unquote_plus(currency_data["name"][0]).strip()
            sign = unquote_plus(currency_data["sign"][0]).strip()

            Validator.validate_post_currencies_controller(code, name, sign)
            self._dao.add_new_currency(code=code, name=name, sign=sign)
            currency_dto = self._dao.get_currency_by_code(code)
            return ResponseDTO(201, currency_dto)
        except ValidationError:
            return ResponseDTO(400, ExceptionDTO(ValidationError()))
        except (KeyError, IndexError, InvalidCurrencyRequestError):
            return ResponseDTO(400, ExceptionDTO(MissingFormFieldError()))
        except sqlite3.IntegrityError:
            response = ResponseDTO(409, ExceptionDTO(CurrencyAlreadyExistsError()))
            return response
        except Exception:
            response = ResponseDTO(500, ExceptionDTO(DatabaseUnavailableError()))
            return response
