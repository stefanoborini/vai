from vixtk import core

class BufferList(core.VObject):
    def __init__(self):
        self._buffer_list = []
        self._current_buffer = None

        self.currentBufferChanged = core.VSignal(self)

    def buffers(self):
        return self._buffer_list

    def add(self, buffer):
        self._buffer_list.append(buffer)
        return buffer

    def select(self, buffer):
        if buffer not in self._buffer_list:
            raise Exception("Buffer not in BufferList")

        if buffer != self._current_buffer:
            old_buffer = self._current_buffer
            self._current_buffer = buffer
            self.currentBufferChanged.emit(old_buffer, self._current_buffer)

        return self._current_buffer

    def addAndSelect(self, buffer):
        self.add(buffer)
        return self.select(buffer)

    def replaceAndSelect(self, old_buffer, new_buffer):
        if old_buffer not in self._buffer_list:
            raise Exception("Buffer not in BufferList")

        index = self._bufferIndex(old_buffer)
        self._buffer_list.remove(old_buffer)
        self._buffer_list.insert(index, new_buffer)
        return self.select(new_buffer)

    def current(self):
        return self._current_buffer

    def selectNext(self):
        if self.current() is None:
            return
        index = (self._bufferIndex(self.current()) + 1) % len(self._buffer_list)
        return self.select(self._buffer_list[index])

    def selectPrev(self):
        if self.current() is None:
            return
        index = (self._bufferIndex(self.current()) - 1) % len(self._buffer_list)
        return self.select(self._buffer_list[index])

    def _bufferIndex(self, buffer):
        return self._buffer_list.index(buffer)

