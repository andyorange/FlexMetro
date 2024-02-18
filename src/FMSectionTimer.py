from typing import List, Callable
from numpy import linspace
import logging
from src.FMBase import FMBarElement, FMSection, FMTickPositions, FMSelection, FMSectionDict
import threading

"""
This is the interface signature for the timer callback:

section_info: FMBarElement, cnt: int, tick_start: List[int], ignore_subbeats: bool | None=None
"""


def ctest(section_info: FMBarElement, cnt: int, tick_start: List[int], ignore_subbeats: bool | None=None) -> bool:
    print(f"{section_info.nom}:{section_info.denom}, {cnt}")
    if not ignore_subbeats:
        if cnt in section_info.subbeats:
            print("  ..subbeat")
    return True


# using this here as a base for the thread based periodic timer: https://gist.github.com/cypreess/5481681
class FMSectionTimer(object):
    """
    Python periodic Thread using Timer with instant cancellation

    The tick_timer should be short enough to not overlap with the tempo. Otherwise, things get out of control.
    """

    def __init__(self,
                 sections: FMSection | FMSectionDict, continuous_sections: bool, callback: Callable | None=None):
        self.sections = {"1": sections} if isinstance(sections, FMSection) else sections
        self.cont = continuous_sections
        # continuous_sections: sections are a sequence. There may be gaps in bars, but subsequent sections are strictly monotonically increasing.
        #  Repeat brackets with overlapping bar numbers need to be encoded as individual sections
        #  If false: sections can have arbitraty bar numbers.
        # subbeats are the beats where the "sublevel" metronome circle should light up. Built from beats
        self.timers = {
            name: FMSectionTimer.CreateMeasureTempi(section) for name, section in self.sections.items()
        }
        self.active_sections = []  # selected ones.
        self.compute_section_data()
        self.tick_start: int = FMTickPositions.T_none  # ticking beat
        self.callback = callback

        self._cnt_beat = 0
        self._cnt_measure = 0
        self._beat_idx = 0
        self._cnt_section = 0
        
        self._stop = False
        self._current_timer = None
        self._schedule_lock = threading.Lock()

    def compute_section_data(self) -> None:
        prev_end = -1
        for section in self.sections:
            if self.cont:
                if section.start < 0:  # continuous sections
                    section.start = prev_end
                    section.end = max(section.start, section.start + section.len - 1)
                else:
                    section.start -= 1  # users count from 1 to x, computers from 0 to x-1
                    section.end -= 1
                    section.len = section.end - section.start + 1
            else:
                if section.start < 0:
                    section.start = 0
                    section.end = max(section.start, section.start + section.len - 1)
                else:
                    section.start -= 1  # users count from 1 to x, computers from 0 to x-1
                    section.end -= 1
                    section.len = section.end - section.start + 1
        return         

    def computer_overlapps(self, sel: FMSelection) -> list:
        section_start = self.sections[sel.section_start]
        section_end = self.sections[sel.section_end]
        
        return []

    @staticmethod
    def CreateMeasureTempi(section: FMSection) -> List[float]:
        tempi = linspace(section.bars.tempo_bar_start, section.bars.tempo_bar_end, section.bars.nom*section.num_bars)
        timers = [60.0/(tempo*section.bars.denom/section.bars.base_beat) for tempo in tempi]
        return timers

    def start(self) -> None:
        self._cnt_beat = 0
        self._cnt_measure = 0
        self._beat_idx = 0
        self._run()  # metronome: the first beat initiates the timer and needs, beats happen BEFORE the countdown!
        #self.schedule_timer()
        return

    def set_callback(self, callback: Callable) -> None:
        self.callback = callback
        return
    
    def resolve_beat(self) -> int:
        if self._cnt_beat == 0:
            return FMTickPositions.T_major
        return FMTickPositions.T_medium if (self._cnt_beat in self.sections.subbeats) else FMTickPositions.T_minor

    def run(self) -> None:
        if self.callback is not None:
            self.callback(self.sections, self._cnt_beat, self.tick_start)
        return

    def _run(self):
        """
        Run desired callback and then reschedule Timer (if thread is not stopped)
        """
        try:
            self.run()
            
        except Exception as exc:
            logging.exception(f"Exception in running periodic thread: {exc}")
        finally:
            #with self.schedule_lock:   # the lock froze the program when cancelling or quitting it
            if not self._stop:
                self.schedule_timer()

    def schedule_timer(self):
        if self._cnt_section >= self.len(self.sections):
            self.cancel()
        if self._cnt_measure >= self.num_measures:
            self._cnt_section += 1
            self._cnt_measure = 0
            return
        self.tick_start = self.resolve_beat()
        self._current_timer = threading.Timer(self.timers[self._beat_idx], self._run)
        self._current_timer.start()
        self._cnt_beat += 1
        self._beat_idx += 1
        if self._cnt_beat >= self.sections.nom:
            self._cnt_beat = 0
            self._cnt_measure += 1


    def cancel(self):
        #with self.schedule_lock:
        self._stop = True
        if self._current_timer is not None:
            self._current_timer.cancel()

    def join(self):
        self._current_timer.join()
