from musicxml.parser import parser
from pathlib import Path
from music21 import converter, stream, meter, tempo, expressions
from dataclasses import dataclass


@dataclass
class TempoExpr:
    xtempo: list
    xacc: list
    xrit: list


class FMTempoParser:
    def __init__(self, file_path: str | Path) -> None:
        #self.xml = parser.parse_musicxml(file_path)
        self.score = converter.parse(file_path)
        self.measures = self._get_measure_data()
        self.sig_changes_at, self.bar_offsets, self.sig_values = self._get_offsets_and_signature_changes()
        self.base_beat = self._get_base_beat(self.sig_values[0])
        self.tempo_expr = self._get_tempo_expression()
        print(self.sig_changes_at)

    def _get_measure_data(self):
        part = self.score.parts.first()
        measures = part.measures(0, None)
        return measures.getElementsByClass(stream.Measure)

    def _get_offsets_and_signature_changes(self) -> list:
        assert(self.measures is not None)
        part = self.score.parts.first()
        signatures = part.getTimeSignatures()
        signatures_at = [sig.offset for sig in signatures]  # offsets for signature changes
        offsets = [measure.offset for measure in self.measures]  # measure start offsets
        signatures_bar = [offsets.index(offs) for offs in signatures_at]  # get measure numbers of signature changes
        return signatures_bar, offsets, signatures.elements
    
    def _get_tempo_expression(self):
        assert(self.measures is not None)
        ret = {}
        for bar in self.measures:
            tmarks = [el for el in bar.elements if isinstance(el, tempo.MetronomeMark)]
            accs = [el for el in bar.elements if isinstance(el, expressions.TextExpression) and "accel" in el.content]
            rits = [el for el in bar.elements if isinstance(el, expressions.TextExpression) and "rit" in el.content]
            if (len(tmarks) + len(accs) + len(rits) > 0):
                expr = TempoExpr(xtempo=tmarks, xacc=accs, xrit=rits)
                ret.update({bar.measureNumber: expr})
        return ret

    def _get_base_beat(self, sig: meter.TimeSignature) -> int:
        ref_bar = sig.measureNumber
        beats = self.bar_offsets[ref_bar] * sig.denominator  # ref_bar is correct, not ref_bar-1.
        return int(beats/sig.numerator)
    
    # get those tempo marks that match new bars
    def _get_tempo_changes_bar_based(self) -> list:
        tempo_bounds = self.score.metronomeMarkBoundaries()
        return [(idx, tempo) for idx, tempo in enumerate(tempo_bounds) if tempo[0] in self.bar_offsets]

    def create_tempo_transitions(self):
        base_beat = self._get_base_beat(self.sig_values[0])
        tempo_changes = self._get_tempo_changes_bar_based()
        tempo_at_bar = [(tc[1][2].measureNumber,
                         tc[1][2].numberSounding if tc[1][2].numberSounding is not None else tc[1][2].number,
                         bool(tc[1][2].number)) for tc in tempo_changes]
        return tempo_at_bar

