import unittest
from unittest.mock import patch
from src.scores_reader import APIClient


class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.api_client = APIClient(base_url='https://scores.frisbee.pl/test3/ext/watchlive.php/')

    @patch('requests.post')
    def test_post_success(self, mock_post):
        # Mocking the response of requests.post
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.text = 'Success'

        # Calling the `post` method of `APIClient`
        result = self.api_client.post({'key': 'value'})
        # Assert checks
        self.assertEqual(result, 'Success')

    @patch('requests.post')
    def test_post_failure(self, mock_post):
        # Mocking the response of requests.post to simulate a failure
        mock_response = mock_post.return_value
        mock_response.status_code = 404
        mock_response.reason = 'Not Found'

        # Testing if an exception is raised
        with self.assertRaises(Exception) as context:
            self.api_client.post({'key': 'value'})

        self.assertTrue('Failed to fetch data: 404 - Not Found' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
