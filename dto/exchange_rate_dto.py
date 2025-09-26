from dataclasses import dataclass
from dto.currency_dto import CurrencyDTO
from decimal import Decimal


@dataclass
class ExchangeRateDto:
    id: int
    base_currency: CurrencyDTO
    target_currency: CurrencyDTO
    rate: Decimal