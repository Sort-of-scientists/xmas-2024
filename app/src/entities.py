from dataclasses import dataclass
import pandas as pd

@dataclass
class Provider:
    id: int
    commission: float
    conversion: float
    min_sum: float
    max_sum: float
    limit_max: float
    limit_min: float
    processing_time: float
    currency: float

    total_amount: int = 0

    def __repr__(self):
        return str(self.__dict__)

@dataclass
class Payment:
    time: pd.Timestamp
    amount: float
    currency: str
    payment: str
    token: str

    def __repr__(self):
        return str(self.__dict__)