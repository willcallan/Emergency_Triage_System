import unittest
import json
from app import app


class TestHelloWorld(unittest.TestCase):

    def test_hello_world(self):
        with app.test_client() as client:
            result = client.get("/")
            body = result.data.decode('utf-8')
            assert body == "Hello World!"
