from dataclasses import dataclass
from dto.currency_dto import CurrencyDTO


@dataclass
class ExchangeRateResponseDto:
    id: int
    baseCurrency: CurrencyDTO
    targetCurrency: CurrencyDTO
    rate: str
