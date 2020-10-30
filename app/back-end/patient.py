from flask import Blueprint, request

from fhirclient import client
import fhirclient.models.patient as pat
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.humanname import HumanName

from typing import List

from vars import settings
from flasgger.utils import swag_from

patient_endpoint = Blueprint('patient_endpoint', __name__)


def get_default_patient() -> pat.Patient:
    patient = pat.Patient()
    # Set their name
    name = HumanName()
    name.given = ['John']
    name.family = 'Test'
    patient.name = [name]
    # Set their gender
    patient.gender = 'male'
    # Set their birth date
    patient.birthDate = FHIRDate('1950-01-01')
    # Add a phone number
    tele = ContactPoint()
    tele.system = 'phone'
    tele.value = '555-100-9999'
    tele.use = 'home'
    patient.telecom = [tele]

    # Set their ID
    patient.id = '628532'

    return patient


@patient_endpoint.route('/patient/save')
@swag_from('static/patient_save.yml')
def patient_save():
    smart = client.FHIRClient(settings=settings)

    # For now, just generate a default patient
    patient = get_default_patient()

    # If the patient has no ID, insert them into the server
    if patient.id is None:
        status = patient.create(smart.server)
        if status is not None:
            return f'Patient created (no id): {status["id"]}'
        else:
            return 'ERROR: Something went wrong when creating this patient'

    # Search for the patient by their ID
    search = pat.Patient.where(struct={'_id': patient.id})
    patients: List[pat.Patient] = search.perform_resources(smart.server)
    # If a patient with that ID is found, update them
    if len(patients) != 0:
        status = patient.update(smart.server)
        if status is not None:
            return f'Patient updated: {status["id"]}'
        else:
            return 'ERROR: Something went wrong when updating this patient'
        # If no patient with that ID is found, create them
    else:
        status = patient.create(smart.server)
        if status is not None:
            return f'Patient created: {status["id"]}'
        else:
            return 'ERROR: Something went wrong when creating this patient'


@patient_endpoint.route('/patient', methods=['GET'])
@swag_from('static/patient_search.yml')
def patient_search():
    patient_id = request.args.get('id', default='d0190651-b9b0-4513-8f3b-d542319220d1', type=str)

    if not patient_id:
        return ''

    smart = client.FHIRClient(settings=settings)
    # Search for the patient by their id
    search = pat.Patient.where(struct={'_id': patient_id})
    patients: List[pat.Patient] = search.perform_resources(smart.server)
    if len(patients) != 0:
        return patients[0].as_json()
    else:
        return f'ERROR: No patient with ID {patient_id} found'
