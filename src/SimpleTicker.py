from src.FMSectionHandler import FMSectionHandler
from src.FMTickerBase import FMTickerBase, FMBarElement, FMTickPositions
import threading


class FMSimpleTicker(FMTickerBase):
    beat_major: str = "major"
    beat_med: str = "medium"
    beat_minor: str = "minor"
    tick_duration_default = 0.125

    def __init__(self, timer: FMSectionHandler | None=None) -> None:
        super(FMSimpleTicker, self).__init__(timer)
        self.connect_timer()

    # implements the interface to
    def tick_callback(self, section_info: FMBarElement, cnt: int,  tick_start: int, ignore_subbeats: bool | None=None):
        self.state = self.fix_subbeat(tick_start, ignore_subbeats=ignore_subbeats)
        print(f"{section_info.subbeats}, {tick_start}. {self.state}")
        tick_timer = threading.Timer(self.tick_duration, self.run_tick_end)
        tick_timer.start()
        return

    def set_tick_duration(self, duration: float) -> None:
        self.tick_duration = min([self.tick_duration_default, duration*0.8])
        return

    def run_tick_end(self) -> None:
        self.state = FMTickPositions.T_none
        self.update()
        return

    def start_timer(self) -> None:
        self.timer.start()
        return

    def stop_timer(self) -> None:
        self.timer.cancel()
        return

    def connect_timer(self, timer: FMSectionHandler | None=None) -> None:
        if timer is not None:
            self.timer = timer
        if self.timer is not None:
            self.timer.set_callback(self.tick_callback)
        return
