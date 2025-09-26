from http_handling.http_response import HttpResponse


class ResponseBuilder:
    """
    Утилитарный класс для построения HTTP ответов из JSON данных.

    Methods:
        build: Создает HTTP ответ из JSON объекта
    """

    @staticmethod
    def build(response_json):
        """
         Преобразует JSON ответ в HTTP ответ.

         Args:
             response_json: Объект JSON ответа с полями:
                 - status_code (int): HTTP статус код
                 - data (str): JSON строка с данными

         Returns:
             HttpResponse: Объект HTTP ответа с установленными статусом и телом

         Note:
             Кодирует JSON строку в байты для отправки по HTTP
         """
        return HttpResponse(
            status_code=response_json.status_code,
            body=response_json.data.encode("utf-8"),
        )
