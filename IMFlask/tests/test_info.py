"""
Info API Test Case
"""
import unittest
from unittest import mock
from app import create_flask_app
from config import TestConfig
from tests.mock import Mock


class InfoTestCase(unittest.TestCase):
    """Calculator Test Case"""

    def setUp(self) -> None:
        self.app = create_flask_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    @mock.patch(
        'model.mongodb.Log.get_log',
        return_value=Mock.get_log(0, 10)
    )
    def test_get_log(self, *args):
        """Test Log API"""
        resp = self.client.get('/sample/log')
        self.assertEqual(resp.status_code, 200)

    @mock.patch(
        'model.mongodb.MasterConfig.get_author',
        return_value=Mock.get_author()
    )
    def test_get_author(self, *args):
        """Test Author API"""
        resp = self.client.get('/sample/author')
        self.assertEqual(resp.status_code, 200)

    @mock.patch('model.mongodb.MasterConfig.change_author')
    def test_change_author(self, *args):
        """Change Author API"""
        resp = self.client.post("/sample/author", json={'name':'NB'})
        self.assertEqual(resp.status_code, 201)
        resp = self.client.put("/sample/author", json={'name':123})
        self.assertEqual(resp.status_code, 400)
