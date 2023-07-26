import unittest
from flask import Flask
from app import app
class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # app = Flask(__name__, template_folder='templates')
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def test_create_entity(self):
        response = self.app.post('/entity', data={"name": "New Entity"})
        self.assertEqual(response.status_code, 302)

    def test_get_all_entity(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_entity(self):
        response = self.app.get('/view_entity/123')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
