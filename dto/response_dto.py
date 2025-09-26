from dataclasses import dataclass
from typing import Any


@dataclass
class ResponseDTO:
    status_code: int
    dto: Any