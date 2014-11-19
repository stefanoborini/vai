import unittest
from tests import fixtures
from vai.models import Configuration

class TestConfiguration(unittest.TestCase):
    def tearDown(self):
        Configuration._instance = None

    def testDefaultInit(self):
        config = Configuration.instance()
        self.assertEqual(config['colors.status_bar.fg'], 'darkcyan')

    def testInitFromFile(self):

        filename = fixtures.get("example_configuration.rc")

        Configuration.setFilename(filename)
        config = Configuration.instance()

        self.assertEqual(config['colors.status_bar.fg'], 'red')





if __name__ == '__main__':
    unittest.main()
