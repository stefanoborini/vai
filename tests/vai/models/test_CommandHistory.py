import unittest
from vai.models.CommandHistory import CommandHistory
from unittest.mock import Mock

class TestCommandHistory(unittest.TestCase):
    def testCommandHistory(self):
        command_history = CommandHistory()
        command = Mock()
        command1 = command()
        command2 = command()
        command3 = command()
        command4 = command()

        self.assertEqual(command_history.numUndoableCommands(), 0)
        self.assertEqual(command_history.numRedoableCommands(), 0)

        command_history.add(command1)
        command_history.add(command2)
        command_history.add(command3)
        command_history.add(command4)

        self.assertEqual(command_history.numUndoableCommands(), 4)
        self.assertEqual(command_history.numRedoableCommands(), 0)

        self.assertEqual(command_history.prev(), command4)
        self.assertEqual(command_history.numUndoableCommands(), 3)
        self.assertEqual(command_history.numRedoableCommands(), 1)

        self.assertEqual(command_history.prev(), command3)
        self.assertEqual(command_history.numUndoableCommands(), 2)
        self.assertEqual(command_history.numRedoableCommands(), 2)

        self.assertEqual(command_history.prev(), command2)
        self.assertEqual(command_history.numUndoableCommands(), 1)
        self.assertEqual(command_history.numRedoableCommands(), 3)

        self.assertEqual(command_history.prev(), command1)
        self.assertEqual(command_history.numUndoableCommands(), 0)
        self.assertEqual(command_history.numRedoableCommands(), 4)

        self.assertRaises(IndexError, lambda : command_history.prev())
        self.assertEqual(command_history.numUndoableCommands(), 0)
        self.assertEqual(command_history.numRedoableCommands(), 4)

        self.assertEqual(command_history.next(), command1)
        self.assertEqual(command_history.numUndoableCommands(), 1)
        self.assertEqual(command_history.numRedoableCommands(), 3)

        self.assertEqual(command_history.next(), command2)
        self.assertEqual(command_history.numUndoableCommands(), 2)
        self.assertEqual(command_history.numRedoableCommands(), 2)

        command_history.add(command4)
        self.assertEqual(command_history.numUndoableCommands(), 3)
        self.assertEqual(command_history.numRedoableCommands(), 0)

        self.assertRaises(IndexError, lambda : command_history.next())

        self.assertEqual(command_history.numUndoableCommands(), 3)
        self.assertEqual(command_history.numRedoableCommands(), 0)

if __name__ == '__main__':
    unittest.main()
