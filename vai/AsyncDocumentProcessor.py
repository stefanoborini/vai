"""
import process

class AsyncDocumentProcessor:
    def __init__(self, document):
        self._document = document

    def monitor(self, enabled):
        raise NotImplementedError("AsyncDocumentProcess.monitor() must be implemented")

    def runOnce(self):
        raise NotImplementedError("AsyncDocumentProcess.runProcess() must be implemented")

"""
