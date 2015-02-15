import unittest
from vaitk import gui
from vai.models import SyntaxColors
from vai.lexer import token
from unittest.mock import patch
from tests import fixtures


class TestSyntaxColors(unittest.TestCase):
    def testDefault(self):
        schema = SyntaxColors("default", 8)
        self.assertIsNotNone(schema.colorMap())
        self.assertTrue(isinstance(schema.colorMap(), dict))
        self.assertIn(token.Keyword, schema.colorMap().keys())

    def testUnexistentNonDefault(self):
        schema = SyntaxColors("whatever", 8)
        self.assertIsNotNone(schema.colorMap())
        schema_default = SyntaxColors("default", 8)
        self.assertEqual(schema.colorMap(), schema_default.colorMap())

    def testExistentNonEmpty(self):
        with patch('vai.paths.pluginsDir') as mock:
            mock.return_value = fixtures.localDir()

            schema = SyntaxColors("DeepBlue", 8)
            color_map = schema.colorMap()
            self.assertIsNotNone(color_map)
            self.assertEqual(len(color_map), 1)
            self.assertTrue(isinstance(color_map[token.Keyword], tuple))
            self.assertEqual(len(color_map[token.Keyword]), 3)


if __name__ == '__main__':
    unittest.main()
