import unittest
from vaitk import gui
from vai.models import SyntaxColor
from vai.models import SyntaxTokens
from unittest.mock import patch
from tests import fixtures


class TestSyntaxColor(unittest.TestCase):
    def testDefault(self):
        schema = SyntaxColor("default", 8)
        self.assertIsNotNone(schema.colorMap())
        self.assertTrue(isinstance(schema.colorMap(), dict))
        self.assertIn(SyntaxTokens.Keyword, schema.colorMap().keys())

    def testUnexistentNonDefault(self):
        schema = SyntaxColor("whatever", 8)
        self.assertIsNotNone(schema.colorMap())
        schema_default = SyntaxColor("default", 8)
        self.assertEqual(schema.colorMap(), schema_default.colorMap())

    def testExistentEmpty(self):
        with patch('vai.paths.syntaxColorDir') as mock:
            mock.return_value = fixtures.localDir()

            schema = SyntaxColor("colorschema", 8)
            self.assertIsNotNone(schema.colorMap())
            self.assertEqual(len(schema.colorMap()), 0)

    def testExistentNonEmpty(self):
        with patch('vai.paths.syntaxColorDir') as mock:
            mock.return_value = fixtures.localDir()

            schema = SyntaxColor("colorschema2", 8)
            color_map = schema.colorMap()
            self.assertIsNotNone(color_map)
            self.assertEqual(len(color_map), 1)
            self.assertTrue(isinstance(color_map[SyntaxTokens.Name], tuple))
            self.assertTrue(isinstance(color_map[SyntaxTokens.Name][0], gui.VColor))
            self.assertEqual(color_map[SyntaxTokens.Name][1], None)


if __name__ == '__main__':
    unittest.main()
