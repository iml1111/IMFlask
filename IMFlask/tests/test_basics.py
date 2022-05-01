"""
Basics Test Case
"""
import unittest
from flask import current_app
from app import create_flask_app
from config import TestConfig

# TODO: 테스트 케이스 작성 및 Mock 테스트 해보기

class BasicsTestCase(unittest.TestCase):
    '''Basics Test Case'''

    def setUp(self):
        '''전처리 메소드'''
        self.app = create_flask_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        '''후처리 메소드'''
        self.app_context.pop()

    def test_app_exists(self):
        '''Application 검증 테스트'''
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        '''Application 테스트 모드 검증 확인'''
        self.assertTrue(current_app.config['TESTING'])

    def test_index_page(self):
        '''Index Template 테스트'''
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_page_404(self):
        '''404 페이지 테스트'''
        resp = self.client.get('/wrong/url')
        self.assertEqual(resp.status_code, 404)
