from vaitk import core

class BufferList(core.VObject):
    def __init__(self):
        self._buffers = []
        self._current = None

        self.currentBufferChanged = core.VSignal(self)

    @property
    def buffers(self):
        return self._buffers

    def add(self, buffer):
        self._buffers.append(buffer)
        return buffer

    def select(self, buffer):
        if buffer not in self._buffers:
            raise Exception("Buffer not in BufferList")

        if buffer != self._current:
            old_buffer = self._current
            self._current = buffer
            self.currentBufferChanged.emit(old_buffer, self._current)

        return self._current

    def addAndSelect(self, buffer):
        self.add(buffer)
        return self.select(buffer)

    def replaceAndSelect(self, old_buffer, new_buffer):
        if old_buffer not in self._buffers:
            raise Exception("Buffer not in BufferList")

        index = self._bufferIndex(old_buffer)
        self._buffers.remove(old_buffer)
        self._buffers.insert(index, new_buffer)
        return self.select(new_buffer)

    @property
    def current(self):
        return self._current

    def selectNext(self):
        if self.current is None:
            return
        index = (self._bufferIndex(self.current) + 1) % len(self._buffers)
        return self.select(self._buffers[index])

    def selectPrev(self):
        if self.current is None:
            return
        index = (self._bufferIndex(self.current) - 1) % len(self._buffers)
        return self.select(self._buffers[index])

    # Private

    def _bufferIndex(self, buffer):
        return self._buffers.index(buffer)

