from vaitk import core

class Selection:
    def __init__(self):
        self.clear()
        self.changed = core.VSignal(self)

    def clear(self):
        self._start_line = None
        self._end_line = None

    @property
    def start_line(self):
        return self._start_line

    @start_line.setter
    def start_line(self, start_line):
        self._start_line = start_line
        self.changed.emit()

    @property
    def end_line(self):
        return self._end_line

    @end_line.setter
    def end_line(self, end_line):
        self._end_line = end_line
        self.changed.emit()




