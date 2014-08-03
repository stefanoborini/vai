from vixtk import core
import unittest

class TestVSignal(unittest.TestCase):
    def testVSignal(self):
        arg = []
        sender = core.VObject()
        signal = core.VSignal(sender)
        def slot(x):
            arg.append(x)
        signal.connect(slot)

        signal.emit(3)

        self.assertEqual(len(arg), 1)
        self.assertEqual(arg[0], 3)

        signal.disconnect(slot)

        signal.emit(3)

        self.assertEqual(len(arg), 1)
        self.assertEqual(arg[0], 3)

    def testDisconnectNotRegistered(self):
        arg = []
        sender = core.VObject()
        signal = core.VSignal(sender)
        def slot(x):
            arg.append(x)
        signal.disconnect(slot)
