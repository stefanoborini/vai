import unittest
from tests import fixtures
from vai.models import Configuration

class TestConfiguration(unittest.TestCase):
    def tearDown(self):
        Configuration._instance = None

    def testDefaultInit(self):
        config = Configuration.instance()
        self.assertNotEqual(config['colors.status_bar.fg'], None)

    def testInitFromFile(self):

        filename = fixtures.get("example_configuration.rc")

        Configuration.setFilename(filename)
        config = Configuration.instance()

        self.assertNotEqual(config['colors.status_bar.fg'], None)





if __name__ == '__main__':
    unittest.main()
