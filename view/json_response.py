class JsonResponse:
    """
    Класс для представления JSON ответа.

    Attributes:
        status_code (int): HTTP статус код
        data (str): JSON строка с данными ответа
    """

    def __init__(self, status_code: int, data):
        self.status_code = status_code
        self.data = data
