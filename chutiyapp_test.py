import os
import chutiyapp
import unittest
import tempfile
from geoloc import geoloc

class ChutiyappTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.dbasefile = tempfile.mkstemp()
        chutiyapp.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.realpath(self.dbasefile)
        chutiyapp.app.config['TESTING'] = True
        self.app = chutiyapp.app.test_client()
        chutiyapp.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.dbasefile)

    def test_geoloc(self):
        print geoloc.bounds(19.177642499999997, 72.8711192)
        assert True


if __name__ == '__main__':
    unittest.main()