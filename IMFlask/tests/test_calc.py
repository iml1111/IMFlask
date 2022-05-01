"""
Calculator Test Case
"""
import unittest
from random import randint
from app import create_flask_app
from config import TestConfig


class CalculatorTestCase(unittest.TestCase):
    """Calculator Test Case"""

    def setUp(self) -> None:
        self.app = create_flask_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_add_func(self):
        """Add Func Test"""
        for _ in range(10):
            a, b = randint(0, 100), randint(0, 100)
            resp = self.client.get("/sample/add?a=%s&b=%s" % (a, b))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], a + b)

        exp_400 = self.client.get("/sample/add?a=1.1")
        self.assertEqual(exp_400.status_code, 400)

    def test_sub_func(self):
        """Subtract Func Test"""
        for _ in range(10):
            a, b = randint(0, 100), randint(0, 100)
            resp = self.client.get("/sample/subtract?a=%s&b=%s" % (a, b))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], a - b)

        exp_400 = self.client.get("/sample/subtract?a=1.1&b=1")
        self.assertEqual(exp_400.status_code, 400)

    def test_multiply_func(self):
        """Multiply Func Test"""
        for _ in range(10):
            a, b = randint(0, 100), randint(0, 100)
            resp = self.client.get("/sample/multiply?a=%s&b=%s" % (a, b))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], a * b)

        exp_400 = self.client.get("/sample/multiply?a=1.1&b=1")
        self.assertEqual(exp_400.status_code, 400)

    def test_divide_func(self):
        """Divide Func Test"""
        for _ in range(10):
            a, b = randint(1, 100), randint(1, 100)
            resp = self.client.get("/sample/divide?a=%s&b=%s" % (a, b))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], a / b)

        exp_400 = self.client.get("/sample/divide?a=1&b=0")
        self.assertEqual(exp_400.status_code, 400)

