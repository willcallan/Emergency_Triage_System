from flask import Blueprint, request
from flasgger.utils import swag_from
import json
from typing import Tuple, List
from datetime import datetime
from pytz import utc

from fhirclient import client
import fhirclient.models.patient as pat
import fhirclient.models.observation as obs
import fhirclient.models.encounter as enc
import fhirclient.models.practitionerrole as prole
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.humanname import HumanName

from vars import settings, esi_lookup

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


@patient_endpoint.route('/patient/save', methods=['POST'])
@swag_from('static/patient_save.yml')
def patient_save():
    # Get the posted patient
    data_json = request.get_json()
    smart = client.FHIRClient(settings=settings)
    patient = pat.Patient(jsondict=data_json)

    # If the patient has no ID (i.e. entered locally), insert them into the server
    if patient.id is None:
        status = patient.create(smart.server)
        if (
            status is not None
            and 'resourceType' in status
            and status['resourceType'] == 'Patient'
        ):
            return f'Patient created: {status["id"]}'
        else:
            return f'ERROR creating patient:\n{status}'

    # See if the patient is in the FHIR server;
    # This will throw an error if they have an erroneous ID
    searched_patient = pat.Patient.read(patient.id, smart.server)
    # If the patient is in the server, update them
    if searched_patient:
        status = patient.update(smart.server)
        if (
            status is not None
            and 'resourceType' in status
            and status['resourceType'] == 'Patient'
        ):
            return f'Patient updated: {status["id"]}'
        else:
            return f'ERROR updating patient:\n{status}'
    return 'ERROR: Search result for this patient in the server returned null.'


@patient_endpoint.route('/patient', methods=['GET'])
@swag_from('static/patient_search.yml')
def patient_search():
    patient_id = request.args.get('id')

    if not patient_id:
        return ''

    # Get the patient by their id
    smart = client.FHIRClient(settings=settings)
    patient: pat.Patient = pat.Patient.read(patient_id, smart.server)

    # Create the return dictionary from the data
    ret_dict = {}
    if patient:
        # Patient data
        ret_dict['name'] = smart.human_name(patient.name[0])
        ret_dict['age'] = get_age(patient)
        # ESI data
        esi, code, display = get_esi(patient, smart)
        ret_dict['esi'] = esi
        ret_dict['code'] = code
        ret_dict['display'] = display
        # ER data
        ret_dict['checkedin'] = get_checkin_time(patient, smart)
        lastseen, seenby = get_last_seen(patient, smart)
        ret_dict['lastseen'] = lastseen
        ret_dict['seenby'] = seenby
        # Data from project database
        # TODO: Hook this up to the project database, FHIR doesn't store this data
        ret_dict['location'] = 'TODO: Use project database'
        ret_dict['status'] = 'TODO: Use project database'

    return json.dumps(ret_dict, indent=4)


def get_age(patient) -> int:
    """
    Calculate a patient's age.

    :param pat.Patient patient: The patient being measured.
    :returns: The age of the patient in years.
    """
    birthdate = datetime.strptime(patient.birthDate.isostring, '%Y-%m-%d')
    today = datetime.today()
    age = int((today - birthdate).days / 365.2425)
    return age


def get_esi(patient, smart) -> Tuple[str, str, str]:
    """
    Returns data regarding a patient's ESI observation.

    :param pat.Patient patient: The patient being searched for.
    :param client.FHIRClient smart: SMART client.
    :return: ESI rating (1-5), code (FHIR coding), and display (plain text version of code).
    """
    # Search the observations to see if this subject has an ESI rating
    # FIXME: This might cause false values to appear if the patient has an ESI obs from a different hospital visit
    search = obs.Observation.where(struct={'subject': f'Patient/{patient.id}',
                                           'code': '75636-1',               # LOINC code for ESI rating
                                           '_sort': '-date',                # Sort the observations newest-oldest
                                           '_count': '1'})                  # Look at only the most recent observation
    results = search.perform_resources(smart.server)

    # If they do, return the requested ESI data
    if len(results) > 0:
        return esi_lookup[results[0].valueCodeableConcept.coding[0].code]
    # If they don't, return empty values
    else:
        return '', '', ''

def get_checkin_time(patient, smart) -> str:
    """
    Returns how long ago the patient was checked in.

    :param pat.Patient patient: The patient being searched for.
    :param client.FHIRClient smart: SMART client.
    :return: Relative time when the patient checked in (e.g. 9.50 hours ago).
    """
    # Search the encounters for the patient's most recent one
    # FIXME: This might cause false values to appear if the patient has an ER enc from a different hospital visit
    search = enc.Encounter.where(struct={'subject': f'Patient/{patient.id}',
                                         'type': '50849002',                # SNOMED code for ER admission
                                         '_sort': '-date',                  # Sort the encounters newest-oldest
                                         '_count': '1'})                    # Look at only the most recent encounter
    results: List[enc.Encounter] = search.perform_resources(smart.server)

    # If they have one, return the time the encounter started
    if len(results) > 0:
        start = datetime.strptime(results[0].period.start.isostring, '%Y-%m-%dT%H:%M:%S%z')
        now = utc.localize(datetime.utcnow())
        difference = "{:.2f}".format((now - start).total_seconds() / (60 * 60)) # Get difference in hours, to 2 decimal places
        return f'{difference} hours ago'
    # If they don't have one, return empty value
    else:
        return ''


def get_last_seen(patient, smart) -> Tuple[str, str]:
    """
    Returns details about the last time a patient was checked on.

    :param pat.Patient patient: The patient being searched for.
    :param client.FHIRClient smart: SMART client.
    :return: How long ago the patient was seen (e.g. 2 minutes) and by which type of practitioner.
    """
    # Search the observations for the patient's most recent one
    # FIXME: This might cause false values to appear if providers don't encode an obs each time they check on a patient
    search = obs.Observation.where(struct={'subject': f'Patient/{patient.id}',
                                           '_sort': '-date',                # Sort the observations newest-oldest
                                           '_count': '1'})                  # Look at only the most recent observation
    results: List[obs.Observation] = search.perform_resources(smart.server)

    # If they have one...
    if len(results) > 0:
        observation = results[0]
        # Get the time the observation was last updated
        start = datetime.strptime(observation.meta.lastUpdated.isostring, '%Y-%m-%dT%H:%M:%S%z')
        now = utc.localize(datetime.utcnow())
        difference = int((now - start).total_seconds() / 60)  # Get difference in minutes
        # Get the practitioner who issued the observation
        role = get_role(observation, smart)

        return f'{difference} minute{"" if difference == 1 else "s"} ago', role
    # If they don't have one, return empty values
    else:
        return '', ''


def get_role(observation, smart) -> str:
    """
    Returns the role of the practitioner who issued an operation.

    :param obs.Observation observation: The observation being measured.
    :param client.FHIRClient smart: SMART client.
    :return: Role of the practitioner who issued the observation.
    """
    if observation.performer is None:
        return ''

    search = prole.PractitionerRole.where(struct={'practitioner': observation.performer[0].reference})
    results: List[prole.PractitionerRole] = search.perform_resources(smart.server)
    if len(results) > 0:
        if (
            results[0].code is not None
            and results[0].code[0].coding is not None
            and results[0].code[0].coding[0].display is not None
        ):
            return results[0].code[0].coding[0].display
    return ''
