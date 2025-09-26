from abc import ABC


class Controller(ABC):
    """
    Абстрактный базовый класс для всех контроллеров.

    Определяет интерфейс для обработки HTTP-запросов различных методов.
    Каждый дочерний класс должен реализовать методы для обработки конкретных HTTP-методов.
    """

    def _handle_get(self, data: dict):
        """
        Абстрактный метод для обработки GET-запросов.

        Args:
            data (dict): Данные запроса, включая параметры, путь, тело и т.д.
        """
        pass

    def _handle_post(self, data: dict):
        """
        Абстрактный метод для обработки POST-запросов.

        Args:
            data (dict): Данные запроса, включая параметры, путь, тело и т.д.
        """
        pass

    def _handle_patch(self, data: dict):
        """
        Абстрактный метод для обработки PATCH-запросов.

        Args:
            data (dict): Данные запроса, включая параметры, путь, тело и т.д.
        """
        pass

    def handle(self, request_data: dict):
        """
        Основной метод для обработки входящих запросов.

        Маршрутизирует запрос к соответствующему методу обработки на основе HTTP-метода.

        Args:
            request_data (dict): Данные запроса, содержащие:
                - method (str): HTTP-метод ('GET', 'POST', 'PATCH')
                - path (str): Путь запроса
                - body (dict): Тело запроса (для POST/PATCH)
                - query_params (dict): Параметры строки запроса

        Returns:
            ResponseDTO: Объект ответа с соответствующим статус-кодом и данными

        Raises:
            NotImplementedError: Если передан неподдерживаемый HTTP-метод
        """
        if request_data["method"] == "GET":
            return self._handle_get(request_data)
        if request_data["method"] == "POST":
            return self._handle_post(request_data)
        if request_data["method"] == 'PATCH':
            return self._handle_patch(request_data)
