from abc import ABC, abstractmethod, abstractclassmethod
from src.FMBase import FMTickPositions, FMBarElement


class FMTickerBase(ABC):
    def __init__(self) -> None:
        FMTickPositions()
        super(FMTickerBase, self).__init__()

    # implements the interface to 
    @abstractmethod
    def tick_callback(self, section_info: FMBarElement, cnt: int, ignore_subbeats: bool | None=None):
        ...

    @staticmethod
    def fix_subbeat(tick_value: int, ignore_subbeats: bool | None = None) -> int:
        return FMTickPositions.T_minor if (tick_value == FMTickPositions.T_medium) and ignore_subbeats else tick_value

