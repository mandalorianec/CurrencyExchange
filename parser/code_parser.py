class CodeParser:
    """
    Утилитарный класс для извлечения кода валюты из пути URL.

    Methods:
        parse_code: Извлекает код валюты из конца пути
    """

    @staticmethod
    def parse_code(path: str):
        """
         Извлекает код валюты из пути URL.

         Args:
             path (str): Путь URL (например, '/currency/USD' или '/exchangeRate/USDRUB')

         Returns:
             str: Код валюты или пары валют из последней части пути

         Example:
             >>> CodeParser.parse_code('/currency/USD')
             'USD'
             >>> CodeParser.parse_code('/exchangeRate/USDRUB/')
             'USDRUB'
         """
        parts = path.split('/')
        currency_code = parts[-1]
        return currency_code
