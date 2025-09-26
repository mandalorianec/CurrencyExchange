from dataclasses import dataclass

@dataclass
class OwnBaseException(Exception):
    """
    Общий класс для всех исключений
    """
    message: str = "Общая ошибка"

    def __str__(self):
        return self.message