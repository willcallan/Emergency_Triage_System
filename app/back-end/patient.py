from flask import Blueprint, request
from flasgger.utils import swag_from
import json
from typing import List
from datetime import date

from fhirclient import client
import fhirclient.models.patient as pat
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.humanname import HumanName

from vars import settings

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
    patient_id = request.args.get('id', default='a4c45fe9-e586-4de4-b6da-78d72e91a4bb')

    if not patient_id:
        return ''

    # Get the patient by their id
    smart = client.FHIRClient(settings=settings)
    patient: pat.Patient = pat.Patient.read(patient_id, smart.server)

    # Create the return dictionary from the data
    ret_dict = {}
    if patient:
        ret_dict['name'] = smart.human_name(patient.name[0])
        ret_dict['age'] = get_age(patient.birthDate.isostring)

    return json.dumps(ret_dict, indent=4)


def get_age(birthdate):
    """Calculates a person's age from their birthdate

    :param str birthdate: ISO date formatted string
    :returns: The age of the person
    """
    today = date.today()
    age = today.year - int(birthdate[0:4])
    age -= ((today.month, today.day) < (int(birthdate[5:7]), int(birthdate[8:10])))
    return age

