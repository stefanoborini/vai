from ..core.VObject import VObject

class VSignalSpy(VObject):
    def __init__(self, signal):
        self._signal_params = []
        self._signal = signal
        self._signal.connect(self._signalReceived)

    def _signalReceived(self, *args, **kwargs):
        self._signal_params.append( (args, kwargs) )

    def count(self):
        return len(self._signal_params)

    def lastSignalParams(self):
        return self._signal_params[-1]

    def signalParams(self):
        return self._signal_params

