import unittest
from fastapi.testclient import TestClient
from mainset import app, fetch_data_from_api, process_data
from unittest.mock import patch


client = TestClient(app)


class TestMain(unittest.TestCase):
    @patch("mainset.fetch_data_from_api")
    @patch("mainset.process_data")
    def test_get_and_process_data(self, mock_process_data, mock_fetch_data):
        mock_response = {'key': 'value'}
        mock_fetch_data.return_value = mock_response

        mock_processed_data = {'KEY': 'VALUE'}
        mock_process_data.return_value = mock_processed_data

        response = client.get("/data/")

        mock_fetch_data.assert_called_once()
        mock_process_data.assert_called_once_with(mock_response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_processed_data)
