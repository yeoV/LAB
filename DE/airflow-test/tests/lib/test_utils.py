"""
Test code using mocking data
"""

import unittest
import sys
from unittest.mock import patch

from lib import load_es_config, load_hdfs_config


class TestLoadEsConfig(unittest.TestCase):
    @patch("lib.utils.Elasticsearch")
    @patch("lib.utils.Connection.get_connection_from_secrets")
    def test_load_es_config(self, mock_conn, mock_es_client):
        # Airflow connection Mock setting
        print(sys.path)
        conn = mock_conn.return_value
        conn.get_uri.return_value = "http://localhost:39200"
        conn.get_password.return_value = "fake_key"

        # Run create es config func
        es_client = load_es_config()

        # self.assertEqual(es_client.transport.hosts, "https://localhost:39200")
        mock_conn.assert_called_once_with("elasticsearch_default")
        mock_es_client.assert_called_once_with(
            "https://localhost:39200", api_key="fake_key", verify_certs=False
        )

    @patch("lib.utils.InsecureClient")
    @patch("lib.utils.Connection.get_connection_from_secrets")
    def test_hdfs_config(self, mock_conn, mock_hdfs):
        conn = mock_conn.return_value
        conn.get_uri.return_value = "http://user:fake@localhost:9870"
        conn.login = "user"
        conn
        # conn.get_password.return_value = "fake_key"

        load_hdfs_config()

        mock_conn.assert_called_once_with("hdfs_default")
        mock_hdfs.assert_called_once_with("http://user:***@localhost:9870", "user")
