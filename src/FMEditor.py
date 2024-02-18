import flet
from FMBase import FMBarElement


class FMMeasureHandler:
    def __init__(self) -> None:
        # Span of measures with constant meter or with tempo transition
        self.span = {}
        self.span_sequence = []
        # user section such as Coda, Intro, A, ...., whatever the user wants
        self.sections = {}
        
        