from typing import Tuple, ClassVar, List, Annotated, TypedDict
from dataclasses import dataclass
from abc import ABC, abstractmethod, abstractclassmethod


@dataclass
class FMBarElement:
    # bar with nom/denom or of given length in seconds as float
    nom: int|float
    denom: int  # = 0 -> nom
    tempo_bar_start: int
    tempo_bar_end: int
    base_beat: int  # base metronom beat.
    beats: Tuple[int] | Tuple[float] | None  # absolute timepoints if denom == 0
    time_beats: Tuple[float] | None = None   # list of major, medium, minor beats as exact timepoints. Set to None if denom > 0

    default_beats: ClassVar[dict] = {
        (3, 4): (0),
        (3, 8): (0),
        (2, 4): (2),
        (4, 4): (2, 2),
        (5, 8): (3, 2),
        (5, 4): (3, 2),
        (6, 8): (3, 3),
        (7, 4): (3, 2, 2),
        (8, 8): (3, 3, 2),
        (6, 4): (3, 3),
        (3, 2): (3)
    }

    # todo: refactor
    def __post_init__(self):
        assert(self.denom in [0, 1, 2, 4, 8, 16, 32])
        self.nom = int(self.nom) if self.denom > 0 else self.nom
        if self.beats is None:
            if self.denom > 0:
                self.beats = FMBarElement.default_beats.get(tuple((self.nom, self.denom)), (0))
                
            else:
                self.beats= (0)
        else:
            self.beats = [int(beat) if self.denom > 0 else beat for beat in self.beats]
        self.subbeats = [0]
        if self.denom > 0:
            self.time_beats = None
            assert((self.beats == (0)) or (sum(self.beats) == self.nom))
            for beat in self.beats[0:-1]:
                if beat > 0:
                    self.subbeats.append(self.subbeats[-1] + beat)
            self.beat_tempo_factor = self.base_beat * 1.0 / self.nom
        else:
            # no tick outside time windows
            self.beats = [beat for beat in self.beats if beat < self.nom]
            self.subbeats = self.beats  # when time is given, beats are absolute time points and thus are the subbeats, actually
            self.beat_tempo_factor = 1
            assert(len(self.time_beats) == len(self.subbeats))
            assert(sum([1 for x in self.time_beats if x not in [FMTickPositions.T_major, FMTickPositions.T_medium, FMTickPositions.T_minor]]))


class MemberSelector(ABC):
    """
    Small helper class allowing class variables to relief the user from remembering strings or alike. See example below
    """

    # T_ for Type.... change on class level if necessary!
    _prefix: str = "T_"

    @classmethod
    def methods(cls, prefix=None):  # type: ignore[no-untyped-def]
        pref = prefix if prefix is not None else cls._prefix
        return [cls.__dict__[member] for member in cls.__dict__ if member.startswith(pref)]

    @classmethod
    def identifiers(cls, prefix=None):  # type: ignore[no-untyped-def]
        pref = prefix if prefix is not None else cls._prefix
        return [c for c in dir(cls) if c.startswith(pref)]
    
    @classmethod
    def methods_except(cls, exceptions: List[str], prefix=None):
        pref = prefix if prefix is not None else cls._prefix
        return [m for m in cls.methods(prefix=pref) if m not in exceptions]


#todo: later when computing length over sections, remember to use start and end and count the real number of bars. There might be gaps!!
@dataclass
class FMSection:
    name: str
    bars: FMBarElement
    num_bars: int | Annotated[tuple[int], 2]

    def __post_init__(self):
        self.len = self.num_bars if isinstance(self.num_bars, int) else max(self.num_bars)-min(self.num_bars)+1
        # if num_bars is not a tuple, start and end might be determined later automatically when sections are chained
        self.start = -1 if isinstance(self.num_bars, int) else min(self.num_bars)
        self.end = -1 if isinstance(self.num_bars, int) else max(self.num_bars)


class FMTickPositions(MemberSelector):
    T_none: int = -1
    T_major: int = 0
    T_medium: int = 1
    T_minor: int = 2


# todo: implement check that end follows start in active sections
@dataclass
class FMSelection:
    bar_start: int
    bar_end: int
    section_start: str
    section_end: str

FMSectionDict = TypedDict("FMSectionDict", {"name": str, "section": FMSection})