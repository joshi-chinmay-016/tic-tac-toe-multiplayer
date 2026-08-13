from abc import ABC, abstractmethod
from typing import List

class AIPlayer(ABC):
    @abstractmethod
    def get_move(self, board: List[str], ai_symbol: str, opponent_symbol: str) -> int:
        pass
