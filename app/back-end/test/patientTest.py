import unittest
import random
from app import app
import triageDB
import json
from datetime import datetime
from faker import Faker


class PatientTests(unittest.TestCase):

    patients = []
    practitioner_ids = []

    faker = Faker()

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
            body_json = json.loads(body)
            assert body_json['patient']['lastseen'] != ''
            assert body_json['notes'][-1]['author'] == practitioner_id

    def test_update_patient_discharge(self):
        with app.test_client() as client:
            patient = random.choice(self.patients)
            practitioner_id = random.choice(self.practitioner_ids)[0]
            result = client.get("/patient/discharge?id="+patient['id'])
            self.patients = triageDB.getallPatient()
            for testpat in self.patients:
                assert patient['id'] != testpat['id']

    def test_create_patient(self):
        with app.test_client() as client:

            new_patient = '' \
                          '{"address": {"city": "Bethfort", "state": "New Jersey", "street": "122 Jaclyn Ferry"}, ' \
                          '"age": "50",' \
                          '"dob": "2015-10-24T00:00:00", "esi": "5", "firstname": "'+self.faker.last_name()+'", ' \
                          '"gender": "female", "language": "English", "lastname": ' \
                          '"'+self.faker.first_name()+'", "lastseen": "", "location": "", ' \
                          '"maritalstatus": "Married", "name": "Margaret Love", "seenby": ""}'
            body_dict = json.loads(new_patient)
            result = client.post("/patient/save", json=body_dict)
            body = result.data.decode('utf-8')
            print(body)
