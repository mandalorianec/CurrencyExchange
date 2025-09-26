import json
from view.json_response import JsonResponse

class View:
    """
    Класс для преобразования объектов в JSON представление.

    Methods:
        make_json: Преобразует DTO объект в JSON ответ
    """
    @staticmethod
    def make_json(resp):
        """
        Преобразует объект ответа в JSON формат.

        Args:
            resp: Объект ответа с полями status_code и dto

        Returns:
            JsonResponse: JSON ответ с установленным статус кодом

        Note:
            Использует json.dumps с кастомным сериализатором
            для преобразования объектов в словари через __dict__
        """
        json_data = json.dumps(resp.dto, default=lambda o: o.__dict__)
        response = JsonResponse(resp.status_code, json_data)
        return response