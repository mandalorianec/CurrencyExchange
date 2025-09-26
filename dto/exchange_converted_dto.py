from dataclasses import dataclass
from decimal import Decimal

from dto.currency_dto import CurrencyDTO


@dataclass
class ExchangeConvertedDto:
    base: CurrencyDTO
    target: CurrencyDTO
    rate: Decimal
    amount: Decimal
    converted_amount: Decimal
