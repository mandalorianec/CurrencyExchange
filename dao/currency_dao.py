from dao.base_dao import BaseDAO
from exceptions.own_exceptions import CurrencyNotFoundError, CurrencyPairNotFoundError
from dto.currency_pair_dto import CurrencyPairIdDTO

from dto.currency_dto import CurrencyDTO


class CurrencyDao(BaseDAO):
    """
    Data Access Object для операций с валютами в базе данных.

    Обеспечивает CRUD-операции с таблицей Currencies и связанными операциями.

    Methods:
        add_new_currency: Добавляет новую валюту
        get_currencies: Получает список всех валют
        get_currency_by_code: Получает валюту по коду
        get_currency_by_id: Получает валюту по идентификатору
        get_id_by_code: Получает ID валюты по коду
        get_currency_pair_id: Получает идентификаторы пары валют
    """

    def add_new_currency(self, code: str, name: str, sign: str):
        """
        Добавляет новую валюту в базу данных.

        Args:
            code (str): Трехбуквенный код валюты (например, 'USD')
            name (str): Полное название валюты
            sign (str): Символ валюты (например, '$')

        Raises:
            sqlite3.IntegrityError: Если валюта с таким кодом уже существует
            sqlite3.Error: При других ошибках базы данных
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Currencies(code, full_name, sign) VALUES(?, ?, ?)", (code, name, sign,))

    def _read_all(self):
        """
        Внутренний метод для чтения всех валют из базы данных.

        Returns:
            list[CurrencyDTO]: Список DTO объектов всех валют

        Raises:
            sqlite3.Error: При ошибках базы данных
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Currencies")
            rows = cursor.fetchall()
            data = []
        for row in rows:
            dto = CurrencyDTO(row[0], row[1], row[2], row[3])
            data.append(dto)
        return data

    def get_currencies(self):
        """
         Получает список всех валют из базы данных.

         Returns:
             list[CurrencyDTO]: Список DTO объектов всех валют

         Raises:
             sqlite3.Error: При ошибках базы данных
         """
        currencies = self._read_all()
        return currencies

    def get_currency_by_code(self, currency_code):
        """
        Получает валюту по ее коду.

        Args:
            currency_code (str): Трехбуквенный код валюты

        Returns:
            CurrencyDTO: DTO объект валюты

        Raises:
            CurrencyNotFoundError: Если валюта с указанным кодом не найдена
            sqlite3.Error: При других ошибках базы данных
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, code, full_name, sign FROM Currencies WHERE code = ?", (currency_code.upper(),))
            row = cursor.fetchone()
        if row is None:
            raise CurrencyNotFoundError(currency_code.upper())
        dto = CurrencyDTO(*row)
        return dto

    def get_currency_by_id(self, currency_id):
        """
        Получает валюту по ее идентификатору.

        Args:
            currency_id (int): Уникальный идентификатор валюты

        Returns:
            CurrencyDTO: DTO объект валюты

        Raises:
            sqlite3.Error: При ошибках базы данных
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, code, full_name, sign FROM Currencies WHERE id=?", (currency_id,))
            row = cursor.fetchone()
        dto = CurrencyDTO(*row)
        return dto

    def get_id_by_code(self, code: str):
        """
        Получает идентификатор валюты по ее коду.

        Args:
            code (str): Трехбуквенный код валюты

        Returns:
            int: Идентификатор валюты

        Raises:
            CurrencyNotFoundError: Если валюта с указанным кодом не найдена
            sqlite3.Error: При других ошибках базы данных
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Currencies WHERE code=?", (code,))
            row = cursor.fetchone()
        if row is None:
            raise CurrencyNotFoundError(code)
        return row[0]  # id

    def get_currency_pair_id(self, base_code, target_code) -> CurrencyPairIdDTO:
        """
         Получает идентификаторы для пары валют.

         Args:
             base_code (str): Код базовой валюты
             target_code (str): Код целевой валюты

         Returns:
             CurrencyPairIdDTO: DTO с идентификаторами обеих валют

         Raises:
             CurrencyPairNotFoundError: Если одна или обе валюты не найдены
             sqlite3.Error: При ошибках базы данных
         """
        try:
            base_currency_id = self.get_id_by_code(base_code)
            target_currency_id = self.get_id_by_code(target_code)
            currency_pair_dto = CurrencyPairIdDTO(base_currency_id, target_currency_id)
        except CurrencyNotFoundError:
            raise CurrencyPairNotFoundError
        return currency_pair_dto
