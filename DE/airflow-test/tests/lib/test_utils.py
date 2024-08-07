import unittest
from unittest.mock import patch, Mock

from dags.lib import load_es_config


class TestLoadEsConfig(unittest.TestCase):
    @patch("dags.lib.utils.Elasticsearch")
    @patch("dags.lib.utils.Connection.get_connection_from_secrets")
    def test_load_es_config(self, mock_conn, mock_es_client):
        # Airflow connection Mock setting
        conn = mock_conn.return_value
        conn.get_uri.return_value = "http://localhost:39200"
        conn.get_password.return_value = "fake_key"

        # Run create es config func
        es_client = load_es_config()

        print(es_client)

        # self.assertEqual(es_client.transport.hosts, "https://localhost:39200")
        mock_conn.assert_called_once_with("elasticsearch_default")
        mock_es_client.assert_called_once_with(
            "https://localhost:39200", api_key="fake_key", verify_certs=False
        )
