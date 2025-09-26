import sqlite3
import os


class BaseDAO:
    """
    Абстрактный базовый класс для всех Data Access Objects (DAO).

    Предоставляет базовую функциональность для работы с базой данных SQLite,
    включая управление подключениями и пути к базе данных.

    Attributes:
        db_path (str): Абсолютный путь к файлу базы данных
    """

    def __init__(self):
        """
        Инициализирует базовый DAO, определяя путь к базе данных.

        База данных располагается в папке 'database' относительно корня проекта.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        database_dir = os.path.join(os.path.dirname(current_dir), 'database')
        self.db_path = os.path.join(database_dir, 'data.db')

    def _connect(self, timeout: int = 10):
        """
         Создает и возвращает подключение к базе данных.

         Args:
             timeout (int): Таймаут подключения в секундах (по умолчанию 10)

         Returns:
             sqlite3.Connection: Объект подключения к базе данных

         Note:
             Использует контекстный менеджер для автоматического управления подключением.
         """
        return sqlite3.connect(self.db_path, timeout=timeout)

    def read_all(self):
        """Абстрактный метод для чтения всех записей из базы данных."""
        pass
