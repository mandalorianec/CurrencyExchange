from http.server import HTTPServer
from http_handling.http_handler import HttpHandler

# перенаправляем stdout/stderr в файл
# log_file = open("/root/currency-exchange/backend/debug.log", "a", buffering=1)  # line-buffered
# sys.stdout = log_file
# sys.stderr = log_file

if __name__ == '__main__':
    """
    Главный точка входа для запуска HTTP сервера обмена валют.

    Сервер запускается на всех интерфейсах (0.0.0.0) на порту 8001 (или 8000 на деплое)
    и использует кастомный HttpHandler для обработки запросов.

    Configuration:
        HOST: '0.0.0.0' (принимает подключения со всех интерфейсов)
        PORT: 8001 (8000 на деплое)

    Usage:
        Запуск: python main.py
        Доступ: http://193.233.86.137:8000 (внешний адрес)
    """
    HOST, PORT = '0.0.0.0', 8001

    with HTTPServer((HOST, PORT), HttpHandler) as server:
        server.serve_forever()

# http://193.233.86.137:8000
