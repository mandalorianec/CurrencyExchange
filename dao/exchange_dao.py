from decimal import Decimal, ROUND_HALF_UP

from dao.base_dao import BaseDAO
from dao.currency_dao import CurrencyDao
from dto.exchange_rate_dto import ExchangeRateDto
from exceptions.own_exceptions import ExchangeRateNotFoundError, ExchangeRateUpdateError


class ExchangeDao(BaseDAO):
    """
    Data Access Object для операций с курсами обмена валют.

    Обеспечивает CRUD-операции с таблицей ExchangeRates.


    Methods:
        read_all: Получает все курсы обмена
        get_rate_by_codepair: Получает курс обмена по паре валют
        add_new_exchange_rate: Добавляет новый курс обмена
        update_exchange_rate: Обновляет существующий курс обмена
    """

    def read_all(self) -> list[ExchangeRateDto]:
        """
         Получает все курсы обмена из базы данных.

         Returns:
             list[ExchangeRateDto]: Список DTO объектов всех курсов обмена

         Raises:
             sqlite3.Error: При ошибках базы данных

         Note:
             Каждый DTO содержит полную информацию о валютах и курсе обмена.
         """
        _currency_dao = CurrencyDao()
        data = []
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ExchangeRates")
            rows = cursor.fetchall()
        for row in rows:
            base_currency_dto = _currency_dao.get_currency_by_id(row[1])
            target_currency_dto = _currency_dao.get_currency_by_id(row[2])
            rate_dto = ExchangeRateDto(row[0], base_currency_dto, target_currency_dto, Decimal(row[3]))
            data.append(rate_dto)
        return data

    def get_rate_by_codepair(self, base_code: str, target_code: str) -> ExchangeRateDto:
        """
        Получает курс обмена для конкретной пары валют.

        Args:
            base_code (str): Код базовой валюты
            target_code (str): Код целевой валюты

        Returns:
            ExchangeRateDto: DTO объекта курса обмена

        Raises:
            ExchangeRateNotFoundError: Если курс для указанной пары не найден
            sqlite3.Error: При других ошибках базы данных

        Note:
            Значение курса округляется до 2 знаков после запятой.
        """
        currency_dao = CurrencyDao()
        with self._connect() as conn:
            cursor = conn.cursor()
            cur_dto = currency_dao.get_currency_pair_id(base_code, target_code)
            cursor.execute(
                "SELECT ID, base_currency_id, target_currency_id, rate FROM ExchangeRates WHERE base_currency_id=? AND target_currency_id=?",
                (cur_dto.base_currency_id, cur_dto.target_currency_id))
            row = cursor.fetchone()
        if row is None:
            raise ExchangeRateNotFoundError()
        rate_dto = ExchangeRateDto(row[0], currency_dao.get_currency_by_code(base_code),
                                   currency_dao.get_currency_by_code(target_code),
                                   Decimal(row[3]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
        return rate_dto

    def add_new_exchange_rate(self, base_currency_id: int, target_currency_id: int, rate: Decimal):
        """
        Добавляет новый курс обмена в базу данных.

        Args:
            base_currency_id (int): ID базовой валюты
            target_currency_id (int): ID целевой валюты
            rate (Decimal): Значение курса обмена

        Raises:
            sqlite3.IntegrityError: Если курс для этой пары валют уже существует
            sqlite3.Error: При других ошибках базы данных
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ExchangeRates(base_currency_id, target_currency_id, rate) VALUES(?, ?, ?)",
                           (base_currency_id, target_currency_id, str(rate),))

    def update_exchange_rate(self, base_code: str, target_code: str, rate: Decimal) -> None:
        """
        Обновляет значение курса обмена для существующей пары валют.

        Args:
            base_code (str): Код базовой валюты
            target_code (str): Код целевой валюты
            rate (Decimal): Новое значение курса обмена

        Raises:
            ExchangeRateUpdateError: Если курс для указанной пары не найден
            sqlite3.Error: При других ошибках базы данных

        Note:
            Перед обновлением проверяет существование курса.
        """
        try:
            existing_rate = self.get_rate_by_codepair(base_code, target_code)
        except ExchangeRateNotFoundError:
            raise ExchangeRateUpdateError
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE ExchangeRates SET rate = ? WHERE ID = ?", (str(rate), existing_rate.id,))
