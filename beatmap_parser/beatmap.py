import re
from abc import ABC, abstractmethod

from .definitions import s_int
from .errors import FileFormatError
from . import parser


class Section(ABC):

    def __init__(self, name, file):
        self.name = name
        self.file = file

    def find(self):
        while (l := self.file.readline()) and f"[{self.name}]" not in l:
            pass

    def readline(self):
        l = self.file.readline()
        return None if l.isspace() else l

    @abstractmethod
    def parse(self):
        pass


class Difficulty(Section):
    def __init__(self, file):
        super().__init__('Difficulty', file)

    def parse(self):
        self.find()

        ret = {}
        p_entry = r'(.*):(.*)$'

        while l := self.readline():
            if m := re.match(p_entry, l):
                ret[m.group(1)] = float(m.group(2))

        return ret


class TimingPoints(Section):
    def __init__(self, file, px_per_beat):
        super().__init__('TimingPoints', file)
        self.px_per_beat = px_per_beat

    def slider_speed(self, beatlength, current_ms_per_beat):
        ms_per_beat = None
        velocity = 1

        if beatlength > 0:
            current_ms_per_beat = beatlength
            ms_per_beat = beatlength
        else:
            velocity = abs(100 / beatlength)
            ms_per_beat = current_ms_per_beat

        if ms_per_beat == None:
            return None, None

        return self.px_per_beat * velocity / ms_per_beat, current_ms_per_beat

    def parse(self):
        self.find()

        ret = []
        current_ms_per_beat = None

        while l := self.readline():
            vals = l.split(",")

            time, beatlength = s_int(vals[0]), float(vals[1])

            px_per_ms, current_ms_per_beat = self.slider_speed(
                beatlength, current_ms_per_beat)

            if px_per_ms == None:
                continue
            timing_point = (time, px_per_ms)

            if len(ret) and time == ret[-1][0]:
                ret[-1] = timing_point
            else:
                ret.append(timing_point)

        return ret


class HitObjects(Section):

    def __init__(self, file=None, timing_points=[]):
        super().__init__('HitObjects', file)
        self.timing_points = timing_points + [(float('inf'), -1)]

    def parse(self):
        self.find()

        ret = []
        idx = 0
        current_time = 0

        while l := self.readline():
            vals = l.split(",")

            time, hit_type = s_int(vals[2]), int(vals[3])

            while not(self.timing_points[idx + 1][0] > time):
                idx += 1

            x, y, time = parser.hitobject_default(l)
            d_time = time - current_time

            obj = None
            if hit_type & 0b1:
                obj = (x, y, x, y, d_time, 0, 1)
            elif hit_type & 0b10:
                x1, y1, duration, repeat_count = parser.slider(
                    l, self.timing_points[idx])
                obj = (x, y, x1, y1, d_time, duration, repeat_count)
            else:
                obj = (0, 0, 0, 0, 0, 0, 0)

            current_time = time + obj[-2]

            ret.append(obj)

        return ret


def parse_hit_objects(file):
    diff_vals = Difficulty(file).parse()

    if 'SliderMultiplier' not in diff_vals:
        raise FileFormatError('SliderMultiplier not found')

    base_px_per_beat = diff_vals['SliderMultiplier'] * 100
    timing_points = TimingPoints(file, base_px_per_beat).parse()

    return HitObjects(file, timing_points).parse()
