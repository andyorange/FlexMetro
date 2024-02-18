import flet
from src.FMBase import FMBarElement, FMTickPositions
from src.FMTickerBase import FMTickerBase
from src.FMSectionTimer import FMSectionTimer
import threading


class FMCircleTicker(FMTickerBase, flet.UserControl):
    beat_major: str = "major"
    beat_med: str = "medium"
    beat_minor: str = "minor"
    tick_duration_default = 0.125

    """
    This class has 3 circles, a large one to the left, a small one to the right and a less than medium one in the middle.
    The left one ticks on main beats, the middle one on medium beats (if tick_medium is True), the right one on minor beats.
    """
    def __init__(self, page: flet.Page, timer: FMSectionTimer | None=None):
        # todo: update all this on resize
        super(FMCircleTicker, self).__init__()
        self.timer = timer
        self.page = page
        self.connect_timer()
        self.cwidth = page.width
        self.cheight = page.height * 0.4
        self.base_diameter = self.cwidth * 0.3   
        self.diam = [self.base_diameter, self.base_diameter*0.45, self.base_diameter*0.3]
        self.circle_cols_bg = [flet.colors.YELLOW_100, flet.colors.BLUE_100, flet.colors.CYAN_100]
        self.circle_cols_tick = [flet.colors.YELLOW_600, flet.colors.BLUE_600, flet.colors.CYAN_600]
        self.state = FMTickPositions.T_none  # nothing ticking. Other values: 0..len(self.circle_cols_xxx)-1
        self.tick_duration = FMCircleTicker.tick_duration_default
        self.circles = {}
        
    def connect_timer(self, timer: FMSectionTimer | None=None) -> None:
        if timer is not None:
            self.timer = timer
        if self.timer is not None:
            self.timer.set_callback(self.tick_callback)
        return
    
    def set_tick_duration(self, duration: float) -> None:
        self.tick_duration = min([FMCircleTicker.tick_duration_default, duration*0.8])
        return

    def tick_callback(self, section_info: FMBarElement, cnt: int, tick_start: int, ignore_subbeats: bool | None=None) -> None:
        self.state = self.fix_subbeat(tick_start, ignore_subbeats=ignore_subbeats)
        print(f"{section_info.subbeats}, {tick_start}. {self.state}")
        self.update()
        tick_timer = threading.Timer(self.tick_duration, self.run_tick_end)
        tick_timer.start()
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

    def update(self) -> None:
        self.controls[0] = self.build()
        return super().update()

    def build(self) -> flet.Row:
        offset = self.cwidth * 0.05
        pos_x = [offset + (idx * 0.3) * (0.4 * self.cwidth) for idx in [0, 1, 2]]
        row = self.create_circle_row(pos_x, self.base_diameter)
        return row

    def create_circle_row(self, xpos: list, width: int) -> flet.Row:
        items = [
            flet.Container(
                border_radius = flet.border_radius.all(2),
                width = int(self.diam[idx]),
                height = int(self.diam[idx]),
                bgcolor = self.circle_cols_tick[idx] if idx == self.state else self.circle_cols_bg[idx],
                shape = flet.BoxShape.CIRCLE
            )
            for idx, posx in enumerate(xpos)
        ]
        return flet.Row(spacing=8, controls=items)

    def __del__(self):
        self.timer.cancel()
        super().__del__()

