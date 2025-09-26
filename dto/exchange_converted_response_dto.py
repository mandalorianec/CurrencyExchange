from dataclasses import dataclass
from dto.currency_dto import CurrencyDTO


@dataclass
class ExchangeConvertedResponseDto:
    baseCurrency: CurrencyDTO
    targetCurrency: CurrencyDTO
    rate: str
    amount: str
    convertedAmount: str
