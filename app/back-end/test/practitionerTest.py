import unittest
import json
from app import app


class PractitionerTests(unittest.TestCase):

    def test_default_practitioners(self):
        with app.test_client() as client:
            result = client.get("/practitioner")
            body = result.data.decode('utf-8')
            print(body)
            assert 'Dr. Rudy Bayer' in body

    def test_single_practitioner(self):
        with app.test_client() as client:
            result = client.get("/practitioner?id=2ee48909-f016-4f03-a7c8-62f525b54269")
            body = result.data.decode('utf-8')
            print(body)
            assert 'Dr. Rudy Bayer' in body
