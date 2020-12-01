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
import fhirclient.models.fhirreference as ref
import fhirclient.models.codeableconcept as conc
import fhirclient.models.coding as cde
from fhirclient.models.humanname import HumanName
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.address import Address
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from dateutil.relativedelta import relativedelta
import json

from vars import settings, esi_lookup, marital_status_lookup

patient_endpoint = Blueprint('patient_endpoint', __name__)


# region URL Functions

@patient_endpoint.route('/patient/save', methods=['POST'])
@swag_from('static/patient_save.yml')
def patient_save():
    """
    Creates and saves a patient into the FHIR server.
    If an ID is provided, updates the patient in the FHIR server instead.
    """

    import fhirclient.models.practitioner as pract
    from triageDB import addPatientEvent, getPatientDetailIdFromFhir, updatePatientDetail, translateFhirIdtoLocalId, updateLastSeen
    from vars import default_events, reverse_esi_lookup
    import dateutil.parser

    # region Nested Functions
    def create_marital_status(term):
        """
        Returns a maritalStatus CodeableConcept based on the term passed in.

        :param str term: The human-readable term for the marital status.
        :returns: The maritalStatus CodeableConcept, or None.
        """
        if term == '':
            return None

        ms = CodeableConcept()
        ms_data = marital_status_lookup[term]
        ms.coding = [Coding({'system': 'http://terminology.hl7.org/CodeSystem/v3-MaritalStatus', 'code': ms_data[0], 'display': ms_data[1]})]
        ms.text = ms.coding[0].display
        return ms

    def create_address(addr):
        """
        Returns an Address based on the data passed in.

        :param dict addr: A dictionary that can contain: street, city, state, and country.
        :returns: The FHIR Address.
        """
        address = Address()
        if 'street' in addr:
            address.line = [addr['street']]
        if 'city' in addr:
            address.city = addr['city']
        if 'state' in addr:
            address.state = addr['state']
        if 'country' in addr:
            address.country = addr['country']
        return address

    def modify_patient(pt, data) -> pat.Patient:
        """
        Updates a patient object with data.

        :param pat.Patient pt: The patient being modified.
        :param dict data: The input data as a JSON dict:
            {id = '',
            firstname: '',
            lastname: '',
            gender: 'male | female | other | unknown',
            dob: 'YYYY-MM-dd',
            email: '',
            contactNumber:'',
            address:'',
            language: 'examples at https://www.hl7.org/fhir/valueset-languages.html'}
        :returns: The updated version of the patient
        """
        if 'firstname' in data:
            pt.name[0].given[0] = data['firstname']
        if 'lastname' in data:
            pt.name[0].family = data['lastname']
        if 'dob' in data and data['dob'] != pt.birthDate.isostring:
            pt.birthDate = FHIRDate(data['dob'])
        if 'gender' in data:
            pt.gender = data['gender']
        if 'maritalstatus' in data:
            if create_marital_status(data['maritalstatus']):
                pt.maritalStatus = create_marital_status(data['maritalstatus'])
        if 'address' in data:
            new_address = create_address(data['address'])
            if not pt.address:
                pt.address = [new_address]
            else:
                pt.address.append(new_address)
        if 'language' in data:
            pt.language = data['language']
        if 'email' in data:
            # TODO: Implement, try to check if email is in the object already
            pass
        if 'contactNumber' in data:
            # TODO: Implement, try to check if contactNumber is in the object already
            pass

        return pt

    def update_all_patient_data(data, smart):

        # Update patient info
        patient_data = data['patient']
        detail_id = getPatientDetailIdFromFhir(patient_data['id'])[0][0]
        patient: pat.Patient = pat.Patient.read(patient_data['id'], smart.server)
        patient = modify_patient(patient, data)
        db_id = translateFhirIdtoLocalId(patient_data['seenby'], pract.Practitioner())[0][0]
        pat_db_id = translateFhirIdtoLocalId(patient_data['id'], pat.Patient())[0][0]

        try:
            last_seen_date = dateutil.parser.parse(patient_data['lastseen'])
        except:
            last_seen_date = None

        updatePatientDetail(pat_db_id,
                            db_id,
                            patient_data['location'],
                            reverse_esi_lookup[patient_data['esi']][0],
                            last_seen_date)

        status = patient.update(smart.server)


        # Create Notes

        last_seen_update = False

        for notes in data['notes']:
            if 'id' not in notes:
                addPatientEvent(detail_id, default_events['NOTE'], notes['note'], notes['author'])
                last_seen_update = True

        if last_seen_update:
            updateLastSeen(patient_data['id'])

        return status

    # endregion

    # Get the posted patient
    data_json = request.get_json()

    if data_json:
        smart = client.FHIRClient(settings=settings)

        if 'patient' in data_json:  # This signals that we are getting the big multi-part patient object
            patient_data = data_json['patient']
            # If the patient has no ID (i.e. entered locally), insert them into the server
            if 'id' not in patient_data or patient_data['id'] == '':
                patient = populate_patient(patient_data)
                status = patient.create(smart.server)
                create_encounter(status['id'],smart)
                insert_patient_details(status['id'])
            else:
                # If the patient does have an ID (i.e. they are in the FHIR server), update them
                status = update_all_patient_data(data_json, smart)

        if (
            status is not None
            and 'resourceType' in status
            and status['resourceType'] == 'Patient'
        ):
            return jsonify(status['id'])
        else:
            return jsonify(status)
    else:
        return ''


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

    notes, history = get_patient_history_and_notes(patient)

    all_data = compile_patient_data(
        get_patient_data(patient, None, smart),
        history,
        notes,
        get_patient_contacts(patient, smart))

    return jsonify(all_data)


@cross_origin()
@patient_endpoint.route('/patient/discharge', methods=['GET'])
def patient_discharge():
    """
    Searches for a patient by ID, returns a dict of the patient triage data.
    """
    from triageDB import getallPatient
    from triageDB import dischargePatient
    patient_id = request.args.get('id')

    if not patient_id:
        return jsonify("")

    dischargePatient(patient_id)

    return jsonify("OK")


@patient_endpoint.route('/patient/search', methods=['GET'])
def patient_search_no_id():
    """
    Searches for a patient by name and dob, returns a dict of the patient triage data.
    """
    from triageDB import patientExistsInDB
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
        if patientExistsInDB(p.id):
            ret_list.append(get_patient_data(p, None, smart))

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
            address:'{street: '', city: '', state: '', country: ''}',
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


def get_patient_data(patient, database_record, smart) -> dict:
    """
    Returns dict object for a patient (according to front-end specifications).

    :param pat.Patient patient: The patient being measured.
    :param client.FHIRClient smart: SMART client.
    :return: Dict of the patient's data.
    """

    patient_dict = {}
    if patient:

        # Get patient details
        if database_record is not None:
            details = {"location" : database_record.patientcurrentlocation,
            "esi" : database_record.esi,
            "firstencounterdate": database_record.firstencounterdate,
            "lastseen": database_record.lastseen if database_record.lastseen is not None else "" ,
            "dischargedate": database_record.dischargedate if database_record.dischargedate is not None else "",
            "seenBy": database_record.triagepractionerid if database_record.triagepractionerid is not None else ""}
        else:
            details = get_patient_details(patient.id)

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
        patient_dict['esi'] = esi_lookup[details['esi']][0]
        patient_dict['code'] = esi_lookup[details['esi']][1]
        patient_dict['display'] = esi_lookup[details['esi']][2]
        # ER data
        patient_dict['checkedin'] = get_checkin_time(patient, smart)
        # Data from project database
        patient_dict['lastseen'] = details['lastseen']
        patient_dict['seenby'] = details['seenBy']
        patient_dict['location'] = details['location']

    return patient_dict


def get_patient_history_and_notes(patient):
    from triageDB import getPatientEventsFromFhirId

    notes = []
    history = []

    for row in getPatientEventsFromFhirId(patient.id):
        if row[2] is None:
            history.append({"id": str(row[0]), "author": row[3], "note": row[1], "time": row[4]})
        else:
            notes.append({"id": str(row[0]), "author": row[3], "note": row[2], "time": row[4]})


    return notes, history

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
    address_dict = {}
    addr = patient.address
    if addr:
        if addr[0].line:
            address_dict['street'] = addr[0].line[0] if addr[0].line is not None else ''
        if addr[0].city:
            address_dict['city'] = addr[0].city if addr[0].city is not None else ''
        if addr[0].state:
            address_dict['state'] = addr[0].state if addr[0].state is not None else ''
        if addr[0].country:
            address_dict['country'] = addr[0].country if addr[0].country is not None else ''

    return address_dict


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
    search = enc.Encounter.where(struct={'subject': f'Patient/{patient.id}',
                                         'type': '50849002',                # SNOMED code for ER admission
                                         '_sort': '-date',                  # Sort the encounters newest-oldest
                                         '_count': '1'})                    # Look at only the most recent encounter
    results: List[enc.Encounter] = search.perform_resources(smart.server)
    import dateutil.parser
    # If they have one, return the time the encounter started
    if len(results) > 0:
        start = dateutil.parser.parse(results[0].period.start.isostring)
        now = datetime.now()
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


def get_patient_details(patient_id):
    from triageDB import getPatientDetailsFromFhir
    result = getPatientDetailsFromFhir(patient_id)[0]
    return {"location" : result[0],
            "esi" : result[1],
            "firstencounterdate": result[2],
            "lastseen": result[3] if result[3] is not None else "" ,
            "dischargedate": result[4] if result[4] is not None else "",
            "seenBy": result[5] if result[5] is not None else ""}


def get_all_triage_patients(database_info):

    ret_list = []
    smart = client.FHIRClient(settings=settings)

    for patient_info in database_info:
        patient = pat.Patient.read(patient_info[0], smart.server)
        ret_list.append(get_patient_data(patient, patient_info, smart))

    return ret_list


def compile_patient_data(patient,history,notes,emergency_contacts):

    ret_obj = {}

    ret_obj['patient'] = patient
    ret_obj['history'] = history
    ret_obj['notes'] = notes
    ret_obj['emergencyContacts'] = emergency_contacts

    return ret_obj


def insert_patient_details(patient_id):
    from triageDB import addPatient, addPatientDetail, addPatientEvent
    from vars import locations, default_events

    db_id = addPatient(patient_id)
    # Add a patient detail below with no practitioner (we have not assigned one)
    detail_id = addPatientDetail(db_id, None, locations[0], "LA21755-6", datetime.now(), None, None, True)
    # Add a patient event below from SYSTEM saying when we created the patient
    addPatientEvent(detail_id,default_events['CREATED'],None,0)


def create_encounter(patient_id, smart):
    import fhirclient.models.period as per
    import fhirclient.models.fhirdate as dat
    encounter = enc.Encounter()
    encounter.subject = ref.FHIRReference({'reference': 'Patient/' + patient_id})

    concept = conc.CodeableConcept()
    code = cde.Coding()
    code.system = "http://snomed.info/sct"
    code.code = "50849002"
    code.display = "Emergency room admission (procedure)"
    concept.coding = [code]
    encounter.type = [concept]

    code = cde.Coding()
    code.system = "http://terminology.hl7.org/CodeSystem/v3-ActCode"
    code.code = "AMB"
    encounter.class_fhir = code
    encounter.status = 'arrived'

    period = per.Period()
    date_start = dat.FHIRDate()
    date_start.date = datetime.now()
    period.start = date_start
    encounter.period = period

    status = encounter.create(smart.server)
    return status['id']
