import random

from flask import Blueprint, request
from flasgger.utils import swag_from
from typing import Tuple, List
from datetime import datetime
from pytz import utc

from flask_cors import CORS, cross_origin
from flask import jsonify

from fhirclient import client
import fhirclient.models.patient as pat
import fhirclient.models.observation as obs
import fhirclient.models.encounter as enc
import fhirclient.models.practitionerrole as prole
from fhirclient.models.humanname import HumanName
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.address import Address
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.patient import PatientContact
from dateutil.relativedelta import relativedelta
import json

from vars import settings, esi_lookup

patient_endpoint = Blueprint('patient_endpoint', __name__)


# region URL Functions

# TODO: connect this up to the db, and ask Vaneet what type of data he wants to save
@patient_endpoint.route('/patient/save', methods=['POST'])
@swag_from('static/patient_save.yml')
def patient_save():
    """
    Saves a patient into the FHIR server.
    """
    # Get the posted patient
    data_json = request.get_json()
    smart = client.FHIRClient(settings=settings)
    patient = populate_patient(data_json)

    # If the patient has no ID (i.e. entered locally), insert them into the server
    # Return the ID of the patient, or an error message
    status = patient.create(smart.server)
    if (
        status is not None
        and 'resourceType' in status
        and status['resourceType'] == 'Patient'
    ):
        return jsonify(status['id'])
    else:
        return jsonify(status)


@cross_origin()
@patient_endpoint.route('/patient', methods=['GET'])
@swag_from('static/patient_search.yml')
def patient_search_id():
    """
    Searches for a patient by ID, returns a dict of the patient triage data.
    """
    from triageDB import getallPatient
    patient_id = request.args.get('id')

    if not patient_id:
        return jsonify(getallPatient())

    # Get the patient by their id
    smart = client.FHIRClient(settings=settings)
    patient: pat.Patient = pat.Patient.read(patient_id, smart.server)

    # Create the flask return json from the data
    return jsonify(get_patient_data(patient, smart))


@patient_endpoint.route('/patient/search', methods=['GET'])
def patient_search_no_id():
    """
    Searches for a patient by name and dob, returns a dict of the patient triage data.
    """
    patient_first_name = request.args.get('firstname')
    patient_last_name = request.args.get('lastname')
    patient_dob = request.args.get('dob')

    # If nothing is passed, do nothing
    if not patient_first_name and not patient_last_name and not patient_dob:
        return jsonify([])

    # Specify the search parameters
    search_params = {}
    if patient_first_name:
        search_params['given'] = patient_first_name
    if patient_last_name:
        search_params['family'] = patient_last_name
    if patient_dob:
        search_params['birthdate'] = patient_dob

    # Search for all patients who match the search parameters
    smart = client.FHIRClient(settings=settings)
    search = pat.Patient.where(struct=search_params)
    patients = search.perform_resources(smart.server)

    ret_list = []
    for p in patients:



        ret_list.append(data)

    return jsonify(ret_list)

# endregion


# region Functions

def populate_patient(data) -> pat.Patient:
    """
    Returns a Patient resource populated with the input data.

    :param dict data: The input data as a JSON dict:
            {firstname: '',
            lastname: '',
            gender: 'male | female | other | unknown',
            dob: 'YYYY-MM-dd',
            email: '',
            contactNumber:'',
            address:'',
            language: 'examples at https://www.hl7.org/fhir/valueset-languages.html'}
    :return: Patient resource.
    """
    patient = pat.Patient()
    # Fill in their name
    if 'firstname' in data or 'lastname' in data:
        name = HumanName()
        if 'firstname' in data and data['firstname']:
            name.given = [data['firstname']]
        if 'lastname' in data and data['lastname']:
            name.family = data['lastname']
        patient.name = [name]
    # Fill in their gender (male | female | other | unknown)
    if 'gender' in data:
        patient.gender = data['gender']
    # Fill in their birthdate (YYYY-MM-dd)
    if 'dob' in data:
        birthdate = FHIRDate(data['dob'])
        patient.birthDate = birthdate
    # Fill in their contacts
    if 'email' in data or 'contactNumber' in data:
        patient.telecom = []
        if 'email' in data and data['email']:
            email = ContactPoint()
            email.system = 'email'
            email.value = data['email']             # johnsmith@example.com
            patient.telecom.append(email)
        if 'contactNumber' in data and data['contactNumber']:
            phone = ContactPoint()
            phone.system = 'phone'
            phone.value = data['contactNumber']     # 123-456-7890
            patient.telecom.append(phone)
    # Fill in their address ([city, state, country])
    if 'address' in data:
        address = Address()
        if 'street' in data['address']:
            address.line = [data['address']['street']]
        if 'city' in data['address']:
            address.city = data['address']['city']
        if 'state' in data['address']:
            address.state = data['address']['state']
        if 'country' in data['address']:
            address.country = data['address']['country']
        patient.address = [address]
    # Fill in their language (examples at https://www.hl7.org/fhir/valueset-languages.html)
    if 'language' in data:
        patient.language = data['language']

    return patient


def get_patient_data(patient, smart) -> dict:
    """
    Returns dict object for a patient (according to front-end specifications).

    :param pat.Patient patient: The patient being measured.
    :param client.FHIRClient smart: SMART client.
    :return: Dict of the patient's data.
    """

    patient_dict = {}
    if patient:
        # Patient data
        patient_dict['id'] = patient.id
        name, first, last = get_name(patient)       # name
        patient_dict['name'] = name
        patient_dict['firstname'] = first
        patient_dict['lastname'] = last
        bd, age = get_birthdate_and_age(patient)    # birthdate
        patient_dict['dob'] = bd
        patient_dict['age'] = age
        patient_dict['gender'] = get_gender(patient)
        patient_dict['maritalstatus'] = get_marital_status(patient)
        patient_dict['address'] = get_address(patient)
        patient_dict['language'] = get_language(patient)
        # ESI data
        esi, code, display = random_esi() # get_esi(patient, smart)
        patient_dict['esi'] = esi
        patient_dict['code'] = code
        patient_dict['display'] = display
        # ER data
        patient_dict['checkedin'] = random_checkin() # get_checkin_time(patient, smart)
        # Data from project database
        # TODO: Hook this up to the project database, FHIR doesn't store this data
       # result= getPatientDetailById(patient.id)
        lastseen, seenby = random_lastseen() # get_last_seen(patient, smart)
        patient_dict['lastseen'] = lastseen
        patient_dict['seenby'] = seenby
        patient_dict['location'] = random.choice(['Waiting room', 'Room 101', 'Room 113', 'Room 204', 'ICU'])
        patient_dict['status'] = random.choice(['1', '2', '3', '4'])

    all_data = compile_patient_data(
        patient_dict,
        get_patient_history(patient, smart),
        get_patient_notes(patient, smart),
        get_patient_contacts(patient, smart),
        [])

    return all_data


def get_patient_history(patient, smart):
    return [{"time": "2020-11-26 12:00:00", "practitioner": "Dr. Drson", "reason": "ache"}]


def get_patient_notes(patient, smart):
    return [{"time": "2020-11-26 12:00:00", "practitioner": "Dr. Drson", "note": "The patient is fine"}]


def get_patient_contacts(patient, smart):
    ret_array = []
    if patient.contact is not None:
        for contact in patient.contact:
            contact_dict = {}
            contact_dict['name'] = smart.human_name(contact.name)
            contact_dict['gender'] = contact.gender
            contact_dict['address'] = get_contact_address(contact)
            contact_dict['phone'] = contact.telecom[0].value
            contact_dict['relationship'] = contact.relationship[0].text
            ret_array.append(contact_dict)

    return ret_array


def get_patient_observations(patient,smart) -> dict:
    return {}


def get_name(patient) -> (str, str, str):
    """
    Returns a patient's name.

    :param pat.Patient patient: The patient being measured.
    :returns: The name of the patient: full, first, last.
    """
    if patient.name:
        name = []
        first = ''
        last = ''
        if patient.name[0].given:
            first = patient.name[0].given[0]
            name.append(first)
        if patient.name[0].family:
            last = patient.name[0].family
            name.append(last)
        return ' '.join(name), first, last
    return '', '', ''


def get_birthdate_and_age(patient) -> (str, str):
    """
    Calculate a patient's age.

    :param pat.Patient patient: The patient being measured.
    :returns: The birthdate and age of the patient in years.
    """
    import dateutil.parser
    if patient.birthDate:
        birthdate = dateutil.parser.parse(patient.birthDate.isostring)
        today = datetime.today()
        age = relativedelta(today, birthdate).years
        return patient.birthDate.isostring, str(age)
    return '', ''


def get_gender(patient) -> str:
    """
    Returns a patient's gender.

    :param pat.Patient patient: The patient being measured.
    :returns: The gender of the patient.
    """
    if patient.gender:
        return patient.gender
    return ''


def get_marital_status(patient) -> str:
    """
    Returns a patient's marital status.

    :param pat.Patient patient: The patient being measured.
    :returns: The marital status of the patient.
    """
    if patient.maritalStatus:
        return patient.maritalStatus.coding[0].display
    return ''


def get_address(patient) -> str:
    """
    Returns a patient's primary address.

    :param pat.Patient patient: The patient being measured.
    :returns: The address of the patient.
    """
    address_list = []
    addr = patient.address
    if addr:
        if addr[0].line:
            address_list.append(addr[0].line[0])
        if addr[0].city:
            address_list.append(addr[0].city)
        if addr[0].state:
            address_list.append(addr[0].state)
        if addr[0].country:
            address_list.append(addr[0].country)
        if address_list:
            return ', '.join(address_list)
    return ''


def get_contact_address(contact) -> str:
    """
    Returns a contact's address.

    :param pat.Patient.contact: The patient being measured.
    :returns: The address of the contact.
    """
    address_list = []
    addr = contact.address
    if addr:
        if addr.city:
            address_list.append(addr.city)
        if addr.state:
            address_list.append(addr.state)
        if addr.country:
            address_list.append(addr.country)
        if address_list:
            return ', '.join(address_list)
    return ''


def get_language(patient) -> str:
    """
    Returns a patient's language.

    :param pat.Patient patient: The patient being measured.
    :returns: The language of the patient.
    """
    if patient.language:
        return patient.language
    return ''


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

# endregion


# ---TEMP CODE---
def random_esi():
    code = random.choice(list(esi_lookup))
    return esi_lookup[code]


def random_checkin():
    return random.choice(['1 hour ago', '2 hours ago', '3 hours ago', '30 minutes ago'])


def random_lastseen():
    return random.choice(['0 minutes ago', '1 minute ago', '2 minutes ago', '3 minutes ago']), random.choice(['Doctor', 'Nurse'])


def get_all_triage_patients(default_ids):

    ret_list = []
    smart = client.FHIRClient(settings=settings)

    for pat_id in default_ids:
        patient = pat.Patient.read(pat_id[1], smart.server)
        ret_list.append(get_patient_data(patient, smart))

    return ret_list


def compile_patient_data(patient,history,notes,emergency_contacts,observations):

    ret_obj = {}

    ret_obj['patient'] = patient
    ret_obj['history'] = history
    ret_obj['notes'] = notes
    ret_obj['emergencyContacts'] = emergency_contacts
    ret_obj['observations'] = observations

    return ret_obj

