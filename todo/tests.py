import unittest
import transaction
from pyramid import testing
from .models import DBSession

class HomePageTest(TestCase):

    def test_home_page_can_handle_post(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = 'a new item'
        response = home_page(request)
        self.assertIn('a new item', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'a new item'})
        self.assertEqual(response.content.decode(), expected_html)

class TestMyViewSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            MyModel,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = MyModel(name='one', value=55)
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_passing_view(self):
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        print(info)
        self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'todo')
        self.assertEqual(info['new_item_text'], 'blah')

class TestMyViewFailureCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            MyModel,
            )
        DBSession.configure(bind=engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_failing_view(self):
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info.status_int, 500)