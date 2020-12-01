import unittest
import random
from app import app
import triageDB
from faker import Faker


class PractitionerTests(unittest.TestCase):

    practitioners = []
    faker = Faker()

    @classmethod
    def setUpClass(self):
        self.practitioners = triageDB.getAllPractitioner()

    def test_search_practitioner(self):
        with app.test_client() as client:
            practitioner = random.choice(self.practitioners)
            result = client.get("/practitioner?id="+practitioner['id'])
            body = result.data.decode('utf-8')
            print(body)
            assert practitioner['id'] in body
