import unittest
import json
from hello import app

class TestHelloWorld(unittest.TestCase):


    def testHelloWorld(self):
        with app.test_client() as client:
            result = client.get("/")
            body = result.data.decode('utf-8')
            assert body == "Hello World!"
