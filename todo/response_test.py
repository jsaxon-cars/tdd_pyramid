import unittest
from webtest import TestApp

class TestBasicSite(unittest.TestCase):

    def setUp(self):
        from pyramid.paster import get_app
        self.app = get_app('development.ini')
        self.testapp = TestApp(self.app)

    def tearDown(self):
        self.testapp = TestApp(self.app)

    def test_home_page(self):
        res = self.testapp.get('/', status=200)
        assert b'To-Do' in res.body
