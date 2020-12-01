import unittest
import random
from app import app
import triageDB
import json
from datetime import datetime

class PatientTests(unittest.TestCase):

    patients = []
    practitioner_ids = []

    @classmethod
    def setUpClass(self):
        self.patients = triageDB.getallPatient()
        self.practitioner_ids = triageDB.getAllPractitionerIds()

    def test_search_patient(self):
        with app.test_client() as client:
            patient = random.choice(self.patients)
            result = client.get("/patient?id="+patient['id'])
            body = result.data.decode('utf-8')
            print(body)
            assert patient['id'] in body

    def test_update_patient_notes(self):
        with app.test_client() as client:
            patient = random.choice(self.patients)
            practitioner_id = random.choice(self.practitioner_ids)[0]
            result = client.get("/patient?id="+patient['id'])
            body = result.data.decode('utf-8')
            body_json = json.loads(body)
            now = datetime.now()
            new_note = {'author': practitioner_id, 'note': 'test note', 'time': str(now)}
            body_json['notes'].append(new_note)
            body_json['patient']['seenby'] = practitioner_id
            result = client.post("/patient/save", json=body_json)
            body = result.data.decode('utf-8')
            print(body)
            result = client.get("/patient?id=" + patient['id'])
            body = result.data.decode('utf-8')
            print(body)


