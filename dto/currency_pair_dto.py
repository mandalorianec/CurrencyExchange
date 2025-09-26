from dataclasses import dataclass


@dataclass
class CurrencyPairIdDTO:
    base_currency_id: int
    target_currency_id: int
