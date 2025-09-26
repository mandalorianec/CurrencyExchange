from urllib.parse import urlparse, parse_qs


class RequestParser:
    """
    Класс для парсинга HTTP запросов и извлечения структурированных данных.

    Преобразует сырые HTTP запросы в словарь с разобранными компонентами:
    метод, путь, параметры запроса, заголовки и тело.

    Methods:
        parse: Основной метод парсинга запроса
        _parse_body: Внутренний метод для обработки тела запроса
    """

    @staticmethod
    def parse(http_request) -> dict:
        """
        Парсит HTTP запрос и возвращает структурированные данные.

        Args:
            http_request: Объект HTTP запроса от BaseHTTPRequestHandler

        Returns:
            dict: Словарь с разобранными компонентами запроса:
                - method (str): HTTP метод (GET, POST, PATCH)
                - path (str): Путь запроса без trailing slash
                - query_params (dict): Параметры строки запроса
                - headers (dict): Заголовки запроса
                - body (dict | None): Тело запроса (для POST/PATCH) или None

        Example:
            Для запроса: GET /currencies?page=1 HTTP/1.1
            Возвращает: {
                'method': 'GET',
                'path': '/currencies',
                'query_params': {'page': ['1']},
                'headers': {...},
                'body': None
            }
        """
        parsed_url = urlparse(http_request.path)
        base_data = {
            "method": http_request.command,
            "path": parsed_url.path.rstrip("/"),
            "query_params": parse_qs(parsed_url.query),  # ? и &
            "headers": dict(http_request.headers),
            "body": None
        }

        if http_request.command in ["POST", "PATCH"]:
            base_data["body"] = RequestParser._parse_body(http_request)

        return base_data

    @staticmethod
    def _parse_body(http_request):
        """
        Парсит тело HTTP запроса для POST и PATCH методов.

        Args:
            http_request: Объект HTTP запроса

        Returns:
            dict: Словарь с параметрами тела запроса

        Note:
            Ожидает данные в формате application/x-www-form-urlencoded
            Декодирует из UTF-8 и парсит как query string
        """
        content_length = int(http_request.headers.get("Content-Length", 0))
        body = http_request.rfile.read(content_length).decode("utf-8")
        return dict(parse_qs(body))
