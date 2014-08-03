import unittest
from vai.models.EditAreaModel import EditAreaModel

class TestEditAreaModel(unittest.TestCase):
    def setUp(self):
        self._model = EditAreaModel()

    def testDocumentTopPos(self):
        with self.assertRaises(ValueError):
            self._model.document_pos_at_top = (-5,1)
            self._model.document_pos_at_top = (5,-1)
        
if __name__ == '__main__':
    unittest.main()
