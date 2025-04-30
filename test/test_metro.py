# from src.speedParser import SpeedParser
# from threading import Timer
from src.SimpleTicker import FMSimpleTicker
from src.FMSectionHandler import FMSectionHandler
from src.FMBase import FMBarElement, FMSection


def main():
    bar1 = FMBarElement(nom=5, denom=8, tempo_bar_start=52, tempo_bar_end=96, base_beat=8, beats=[2, 3])
    si1 = FMSection("Intro", bars=bar1, num_bars=2)
    bar2 = FMBarElement(nom=2, denom=4, tempo_bar_start=96, tempo_bar_end=96, base_beat=4)
    si2 = FMSection("End", bars=bar2, num_bars=1)

    tmr = FMSectionHandler(si1, 2)
    ticker = FMSimpleTicker(tmr)
    ticker.set_tick_duration(duration=min(tmr.base_timer))
    ticker.connect_timer(tmr)
    ticker.start_timer()
    #pass
    #ticker.stop_timer()

#si = FMBarElement(nom=7, denom=8, tempo_bar_start=52, tempo_bar_end=96, base_beat=8, beats=[2, 3, 2])
# tmr = FMMeasureTimer(si, 2, ctest)
# tmr.start()

# prs = SpeedParser("./Unschuldig - Full score - 01 Flow 1.musicxml")
# trans = prs.create_tempo_transitions()

if __name__ == "__main__":
    main()
