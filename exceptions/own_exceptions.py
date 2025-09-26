from dataclasses import dataclass

from exceptions.base_exception import OwnBaseException


@dataclass
class CurrencyNotFoundError(OwnBaseException):
    """Вызывается, если не удалось найти код валюты в базе данных"""
    message: str = "Валюта не найдена"

    # error_code: int = 404


@dataclass
class ExchangeRateNotFoundError(OwnBaseException):
    """Вызывается, если не удалось найти запрашиваемый обменный курс"""
    message: str = "Обменный курс для пары не найден"

    # error_code: int = 404


@dataclass
class DatabaseUnavailableError(OwnBaseException):
    """Вызывается, если произошла неизвестная ошибка на стороне сервера"""
    message: str = "The database is unavailable"

    def __post_init__(self):
        super().__init__(self.message)

    # error_code: int = 500


@dataclass
class CurrencyAlreadyExistsError(OwnBaseException):
    """Вызывается, если валюта с таким кодом уже существует"""
    message: str = "Валюта с таким кодом уже существует"


@dataclass
class CurrencyPairAlreadyExistsError(OwnBaseException):
    """Вызывается, если валютная пара с таким курсом уже существует"""
    message: str = "Валютная пара с таким кодом уже существует"


@dataclass
class CurrencyPairNotFoundError(OwnBaseException):
    """Вызывается, если одна или обе валюты отсутствуют в БД"""
    message: str = "Одна (или обе) валюта из валютной пары не существует в БД"


@dataclass
class ExchangeRateUpdateError(OwnBaseException):
    """Вызывается при ошибке обновления обменного курса"""
    message: str = "Валютная пара отсутствует в базе данных"


@dataclass
class InvalidCurrencyRequestError(OwnBaseException):
    """Вызывается при валидации коды валюты, если он неверен"""
    message: str = "Код валюты отсутствует в адресе"


@dataclass
class MissingFormFieldError(OwnBaseException):
    """Вызывается, когда в форме отсутствует обязательное поле"""
    message: str = "Отсутствует нужное поле формы"


@dataclass
class InvalidCurrencyPairRequestError(OwnBaseException):
    """Вызывается при валидации пары кода валют, если она неверна"""
    message: str = "Коды валют пары отсутствуют в адресе"


@dataclass
class ValidationError(OwnBaseException):
    """Вызывается валидатором при некорректно введённых данных"""
    message: str = "Некорректный ввод"
