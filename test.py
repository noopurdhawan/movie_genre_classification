import unittest
from flask import Flask
import json

# Import your Flask app
from predict import app


class AppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_predict_genre(self):
        # Create a sample input payload
        payload = {
            'overview': 'A movie about penguins in Antarctica building a spaceship to go to Mars.'
        }

        # Make a POST request to the Flask route
        response = self.app.post('/', json=payload)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response data
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('genre', data)
        genres = data['genre']
        self.assertIsInstance(genres, list)
        self.assertGreater(len(genres), 0)

    def test_bad_request(self):
        # Make a POST request with missing payload
        response = self.app.post('/')

        # Check the response data
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('status', data)
        self.assertEqual(data['status'], 400)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Bad Request')


if __name__ == '__main__':
    unittest.main()
