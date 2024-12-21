from abc import ABC, abstractmethod

from .entities import Provider
from typing import List, Literal


class BaseStrategy:

    def __init__(self):
        pass

    @abstractmethod
    def optimize(self, providers: List[Provider]) -> List[Provider]:
        """
        Возвращает оптимальный порядок провайдеров.
        """
        raise NotImplementedError
    

class GreedyStrategy(BaseStrategy):

    def __init__(self, by: Literal["commission", "processing_time", "conversion"] = "commission"):
        super().__init__()

        self.by = by

    def optimize(self, providers: List[Provider]) -> List[Provider]:
        return sorted(providers, key=lambda provider: getattr(provider, self.by))