import unittest
import json
from app import app


class PatientTests(unittest.TestCase):

    def test_default_patients(self):
        with app.test_client() as client:
            result = client.get("/patient")
            body = result.data.decode('utf-8')
            print(body)
            assert 'Britany' in body

    def test_single_patient(self):
        with app.test_client() as client:
            result = client.get("/patient?id=a4c45fe9-e586-4de4-b6da-78d72e91a4bb")
            body = result.data.decode('utf-8')
            print(body)
            assert 'Britany' in body
