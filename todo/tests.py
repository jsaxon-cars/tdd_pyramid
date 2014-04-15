import unittest
import transaction
from pyramid import testing
from .models import DBSession
from sqlalchemy import create_engine
from .models import (
    Base,
    MyModel
)
from .views import home

#def setupSession():

class TestMyViewSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = MyModel(name='one', value=55)
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_passing_view(self):
        from .views import home
        request = testing.DummyRequest()
        info = home(request)
        self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'todo')


# What exactly are we failing here???
class TestMyViewFailureCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_failing_view(self):
        request = testing.DummyRequest()
        info = home(request)
        self.assertEqual(info.status_int, 500)


class TestPostingNewItemIncludesNewItem(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = MyModel(name='one', value=55)
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_home_page_can_handle_post(self):
        request = testing.DummyRequest(post={'item_text':'a new item'})
        info = home(request)
        self.assertEqual(info, {})
        self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'todo')
