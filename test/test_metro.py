from speedParser import SpeedParser
from threading import Timer
from FlexComponents import FMCircleTicker
from FlexTimer import FMMeasureTimer, ctest
from FMBase import FMBarElement
import flet

def main(page: flet.Page):
    si = FMBarElement(nom=5, denom=8, tempo_bar_start=52, tempo_bar_end=96, base_beat=8, beats=[2, 3])
    si = FMBarElement(nom=2, denom=4, tempo_bar_start=96, tempo_bar_end=96, base_beat=4)
    page.title = "FlexMetro"
    page.update()
    ticker = FMCircleTicker(page)
    tmr = FMMeasureTimer(si, 2)
    ticker.set_tick_duration(duration=min(tmr.timers))
    ticker.connect_timer(tmr)
    page.add(ticker)
    #ticker.update()
    page.update()
    ticker.start_timer()
    #pass
    #ticker.stop_timer()

flet.app(target=main)
#si = FMBarElement(nom=7, denom=8, tempo_bar_start=52, tempo_bar_end=96, base_beat=8, beats=[2, 3, 2])
# tmr = FMMeasureTimer(si, 2, ctest)
# tmr.start()

# prs = SpeedParser("./Unschuldig - Full score - 01 Flow 1.musicxml")
# trans = prs.create_tempo_transitions()


pass