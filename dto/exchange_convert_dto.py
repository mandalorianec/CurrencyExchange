from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ExchangeConvertDto:
    base: str
    target: str
    amount: Decimal

