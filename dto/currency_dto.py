from dataclasses import dataclass


@dataclass
class CurrencyDTO:
    id: int
    code: str
    name: str
    sign: str

