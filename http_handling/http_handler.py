from http.server import BaseHTTPRequestHandler

from dto.exception_dto import ExceptionDTO
from dto.response_dto import ResponseDTO
from exceptions.own_exceptions import DatabaseUnavailableError
from parser.request_parser import RequestParser
from utils.response_builder import ResponseBuilder
from routing.router import Router
from view.view import View


class HttpHandler(BaseHTTPRequestHandler):
    """
    Кастомный HTTP-хэндлер для обработки входящих запросов.

    Наследуется от BaseHTTPRequestHandler и обрабатывает HTTP-запросы,
    маршрутизируя их к соответствующим контроллерам через роутер.

    Поддерживаемые HTTP-методы:
        - GET: Получение данных
        - POST: Создание новых данных
        - PATCH: Обновление существующих данных
        - OPTIONS: Preflight запросы для CORS

    Attributes:
        Унаследованные от BaseHTTPRequestHandler:
            client_address: Адрес клиента
            server: Серверный объект
            headers: Заголовки запроса
            rfile: Входной поток
            wfile: Выходной поток
    """

    def do_GET(self):
        """
        Обрабатывает HTTP GET запросы.

        Вызывается автоматически сервером при получении GET запроса.
        Перенаправляет запрос в общий метод обработки.
        """
        self._handle_request("GET")

    def do_POST(self):
        """
        Обрабатывает HTTP POST запросы.

        Вызывается автоматически сервером при получении POST запроса.
        Перенаправляет запрос в общий метод обработки.
        """
        self._handle_request("POST")

    def do_PATCH(self):
        """
        Обрабатывает HTTP PATCH запросы.

        Вызывается автоматически сервером при получении PATCH запроса.
        Перенаправляет запрос в общий метод обработки.
        """
        self._handle_request("PATCH")

    def do_OPTIONS(self):
        """
        Обрабатывает HTTP OPTIONS запросы для CORS preflight.

        Отправляет заголовки CORS, разрешающие кросс-доменные запросы.
        Используется браузерами для проверки разрешенных методов до отправки основного запроса.
        """
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def _handle_request(self, method: str):
        """
        Основной метод обработки HTTP запросов.

        Выполняет полный цикл обработки запроса:
        1. Парсинг входящего запроса
        2. Поиск соответствующего контроллера через роутер
        3. Выполнение бизнес-логики в контроллере
        4. Преобразование результата в JSON
        5. Построение HTTP ответа
        6. Отправка ответа клиенту

        Args:
            method (str): HTTP метод запроса ('GET', 'POST', 'PATCH')

        Flow:
            Запрос → Парсинг → Роутинг → Контроллер → JSON → HTTP Ответ → Клиент

        Exception Handling:
            Любые необработанные исключения перехватываются и преобразуются
            в ответ 500 Internal Server Error.
        """
        request_data = RequestParser.parse(self)
        controller = Router.find_controller(method, request_data["path"])
        try:
            controller_result = controller.handle(request_data)
        except Exception:
            controller_result = ResponseDTO(500, ExceptionDTO(DatabaseUnavailableError()))
        json_response = View.make_json(controller_result)
        http_response = ResponseBuilder.build(json_response)
        self._write_response(http_response)

    def _write_response(self, response):
        """
        Отправляет HTTP ответ клиенту.

        Устанавливает статус код, заголовки и тело ответа.

        Args:
            response: Объект ответа, содержащий:
                - status_code (int): HTTP статус код
                - body (bytes): Тело ответа в байтах

        Headers:
            - Content-Type: application/json; charset=utf-8
            - Content-Length: Длина тела ответа
            - CORS headers: Разрешения для кросс-доменных запросов
        """
        self.send_response(response.status_code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header("Content-Length", str(len(response.body)))
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(response.body)

    def _set_cors_headers(self):
        """
        Устанавливает заголовки CORS (Cross-Origin Resource Sharing).

        Разрешает кросс-доменные запросы со любых источников (*).

        CORS Headers:
            - Access-Control-Allow-Origin: * (разрешает запросы с любых доменов)
            - Access-Control-Allow-Methods: GET, POST, PATCH, OPTIONS (разрешенные методы)
            - Access-Control-Allow-Headers: Content-Type, X-Requested-With (разрешенные заголовки)
        """
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Requested-With')
