from videtoolkit import core

class BufferList(core.VObject):
    def __init__(self):
        self._buffer_list = []
        self._current_buffer = None

        self.currentBufferChanged = core.VSignal(self)

    def add(self, buffer):
        self._buffer_list.append(buffer)

    def select(self, buffer):
        if buffer not in self._buffer_list:
            raise Exception("Buffer not in BufferList")

        self._current_buffer = buffer
        self.currentBufferChanged.emit(buffer)

    def addAndSelect(self, buffer):
        self.add(buffer)
        self.select(buffer)

    def replaceAndSelect(self, old_buffer, new_buffer):
        if old_buffer not in self._buffer_list:
            raise Exception("Buffer not in BufferList")

        index = self._bufferIndex(old_buffer)
        self._buffer_list.remove(old_buffer)
        self._buffer_list.insert(index, new_buffer)
        self.select(new_buffer)

    def current(self):
        return self._current_buffer

    def selectNext(self):
        index = (self._bufferIndex(self.current()) + 1) % len(self._buffer_list)
        self.select(self._buffer_list[index])

    def selectPrev(self):
        index = (self._bufferIndex(self.current()) - 1) % len(self._buffer_list)
        self.select(self._buffer_list[index])

    def _bufferIndex(self, buffer):
        return self._buffer_list.index(buffer)

