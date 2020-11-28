from typing import List

from flask import Blueprint, request
from datetime import datetime

from flask_cors import CORS, cross_origin
from flask import jsonify

from fhirclient import client
import fhirclient.models.observation as obs
import fhirclient.models.encounter as enc
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.annotation import Annotation
from fhirclient.models.quantity import Quantity

from vars import settings, body_site_lookup, wound_lookup, systems_injury_lookup

observation_endpoint = Blueprint('observation_endpoint', __name__)


# region URL Functions

@observation_endpoint.route('/observation/save', methods=['POST'])
def observation_save():
    """
    Saves an observation into the FHIR server.
    """
    # Get the posted patient
    data_json = request.get_json()
    smart = client.FHIRClient(settings=settings)
    observation = populate_observation(data_json, smart)

    # If the observation did not return anything, tell the user the error
    if not observation:
        return 'Observation was formatted incorrectly.'

    # Return the ID of the observation, or an error message
    status = observation.create(smart.server)
    if (
        status is not None
        and 'resourceType' in status
        and status['resourceType'] == 'Observation'
    ):
        return jsonify(status['id'])
    else:
        return jsonify(status)


@cross_origin()
@observation_endpoint.route('/observations', methods=['GET'])
def observation_search():
    """
    Searches for all observations by patient ID, returns a list of observation dicts.
    """
    patient_id = request.args.get('id')

    # If no id is provided, return nothing
    if not patient_id:
        return ''

    smart = client.FHIRClient(settings=settings)

    # Specify the search parameters
    search_params = {}
    search_params['patient'] = patient_id
    enc_id = get_encounter_id(patient_id, smart)
    if enc_id:
        search_params['encounter'] = enc_id

    # Search for all observations who match the search parameters
    search = obs.Observation.where(struct=search_params)
    observations = search.perform_resources(smart.server)

    ret_list = []
    for o in observations:
        ret_list.append(get_observation_data(o))

    return jsonify(ret_list)

# endregion


# region Functions

def populate_observation(data, smart) -> obs.Observation:
    """
    Returns an Observation resource populated with the input data.

    :param dict data: The input for wound data as a JSON dict:
            {patientID: '',
            bodyPart: '',
            injury: '',
            severity: '' OPTIONAL}
        The input for systems data as a JSON dict:
            {system: '',
            value: '' OPTIONAL}
    :param client.FHIRClient smart: The FHIR client.
    :return: Observation resource.
    """
    # Create a default blank Observation.
    observation = create_blank_observation(data['patientID'], smart)

    # If this is not a wound, it should be a system injury
    if 'system' in data:
        observation = create_systems_observation(data, observation)
    elif 'injury' in data:
        observation = create_injury_observation(data, observation)
    else:
        return None

    # Save the user's notes about this observation
    if 'note' in data:
        gcs_annotation = Annotation()
        gcs_annotation.time = FHIRDate(get_current_time())
        gcs_annotation.text = data['note']
        if observation.note:
            observation.note.append(gcs_annotation)
        else:
            observation.note = [gcs_annotation]

    return observation


def create_blank_observation(patientID, smart) -> obs.Observation:
    """
    Returns a blank Observation resource populated with common data (things like the patient, time, encounter, etc.).
    :param str patientID: The FHIR ID of the patient.
    :param client.FHIRClient smart: The FHIR client.
    :return: Observation resource.
    """
    observation = obs.Observation()
    # Status of the observation (specific values found at https://www.hl7.org/fhir/codesystem-observation-status.html)
    observation.status = 'preliminary'
    # How the observation was conducted
    categoryconcept = CodeableConcept()
    categoryconcept.coding = [Coding(
        {'system': 'http://terminology.hl7.org/CodeSystem/observation-category', 'code': 'exam', 'display': 'exam'})]
    observation.category = [categoryconcept]
    # The patient being observed
    observation.subject = FHIRReference({'reference': 'Patient/' + patientID})
    # The encounter that this observation is part of
    observation.encounter = FHIRReference({'reference': get_encounter_id(patientID, smart)})
    # The time that this observation was first made (times should be in ISO format)
    observation.effectiveDateTime = FHIRDate(get_current_time())
    # The time that this observation was reviewed and approved (times should be in ISO format)
    observation.issued = observation.effectiveDateTime

    return observation


def create_systems_observation(data, observation) -> obs.Observation:
    """
    Returns an Observation resource populated with data about a systems injury.

    :param dict data: The input for systems data as a JSON dict:
            {system: '',
            value: '' OPTIONAL}
    :param obs.Observation observation: A default observation.
    :return: Observation resource.
    """

    # region Nested Functions
    # Retrieved calculation from https://www.ncbi.nlm.nih.gov/books/NBK513298/
    def get_Glasgow_score(values) -> (Quantity, Annotation):
        """
        Returns the Glasgow Score total for eye, verbal, and motor response.

        :param dict values: The input for GCS data as a JSON dict:
            {eye: '',
            verbal: '',
            motor: ''}
            :returns: valueQuantity of GCS score and note explaining score in the form GCSx=ExVxMx.
        """
        # Get valueQuantity
        total = int(values['eye']) + int(values['verbal']) + int(values['motor'])
        gcs_quantity = Quantity()
        gcs_quantity.value = total
        gcs_quantity.unit = 'score'
        gcs_quantity.system = 'http://loinc.org'

        # Get note
        note = ''
        note += 'GCS' + str(total)
        note += '='
        note += 'E' + str(values['eye'])
        note += 'V' + str(values['verbal'])
        note += 'M' + str(values['motor'])
        gcs_annotation = Annotation()
        gcs_annotation.time = FHIRDate(get_current_time())
        gcs_annotation.text = note

        return gcs_quantity, gcs_annotation

    # Using classification from https://litfl.com/major-haemorrhage-in-trauma/
    def get_hemorrhage_class(value):
        """
        Returns the Glasgow Score total for eye, verbal, and motor response.

        :param dict value: The input for GCS data as a str:
               'Class 1' | 'Class 2' | 'Class 3' | 'Class 4'
        :returns: valueQuantity of GCS score and note explaining score in the form GCSx=ExVxMx.
        """
        return value
    # endregion

    # Just in case check
    if data['system'] not in systems_injury_lookup:
        return None

    # Get the data for the system being observed
    system_data = systems_injury_lookup[data['system']]

    # Marking which system this observation is about
    codeconcept = CodeableConcept()
    codeconcept.coding = [Coding({'system': system_data[2], 'code': system_data[0], 'display': system_data[1]})]
    codeconcept.text = codeconcept.coding[0].display
    observation.code = codeconcept

    # Filling in extra info about specific injuries
    if system_data[1] == 'Glasgow coma score total':
        quantity, note = get_Glasgow_score(data['value'])
        observation.valueQuantity = quantity
        observation.note = [note]
    elif system_data[1] == 'Procedure estimated blood loss':
        observation.valueString = get_hemorrhage_class(data['value'])

    return observation


def create_injury_observation(data, observation) -> obs.Observation:
    """
    Returns an Observation resource populated with data about a wound.

    :param dict data: The input for wound data as a JSON dict:
            {patientID: '',
            bodyPart: '',
            injury: '',
            severity: '' OPTIONAL}
    :param obs.Observation observation: A default observation.
    :return: Observation resource.
    """

    # region Nested Functions
    def get_bodysite_concept(term) -> CodeableConcept:
        """
        Returns CodeableConcept for a body part.

        :param str term: The lay term for the body part.
        :return: CodeableConcept with the SNOMED code for that body part.
        """
        bodysite_data = body_site_lookup[term]
        concept = CodeableConcept()
        concept.coding = [Coding({'system': 'http://snomed.info/sct', 'code': bodysite_data[0], 'display': bodysite_data[1]})]
        concept.text = concept.coding[0].display
        return concept

    def get_wound_value_concept(term) -> CodeableConcept:
        """
        Returns CodeableConcept for a wound type.

        :param str term: The lay term for the wound.
        :return: CodeableConcept with the LOINC code for that wound.
        """
        wound_data = wound_lookup[term]
        concept = CodeableConcept()
        concept.coding = [Coding({'system': 'http://loinc.org', 'code': wound_data[0], 'display': wound_data[1]})]
        concept.text = concept.coding[0].display
        return concept
    # endregion

    # Marking that this observation is about a wound
    codeconcept = CodeableConcept()
    codeconcept.coding = [Coding({'system': 'http://loinc.org', 'code': '72300-7', 'display': 'Wound type'})]
    codeconcept.text = codeconcept.coding[0].display
    observation.code = codeconcept
    # The body part that is marked
    observation.bodySite = get_bodysite_concept(data['bodyPart'])
    # The results of the observation (the field used for this changes depending on how the observation was measured)
    observation.valueCodeableConcept = get_wound_value_concept(data['injury'])
    # The severity of the wound
    if 'severity' in data:
        note = Annotation({'time': get_current_time(), 'text': 'Marked severity: ' + str(data['severity'])})
        observation.note = [note]

    return observation


def get_observation_data(observation) -> dict:
    """
    Returns dict object for an observation (according to front-end specifications).

    :param obs.Observation observation: The observation being measured.
    :return: Dict of the observation's data.
    """

    # region Nested Functions
    def get_severity(observation) -> str:
        """
        Returns the severity that was coded for this observation.

        :param obs.Observation observation: The observation being measured.
        :return: The severity (string between 0 and 10).
        """
        if observation.note:
            for annotation in observation.note:
                if annotation.text[0:-2] == 'Marked severity:':
                    return annotation.text[-1:]
        return ''

    def get_GCS_score(observation) -> str:
        """
        Returns the GCS score that was coded for this observation.

        :param obs.Observation observation: The observation being measured.
        :return: The GCS score (string of form GCSx=ExVxMx).
        """
        if observation.note:
            for annotation in observation.note:
                if annotation.text[0:3] == 'GCS':
                    return annotation.text
        return ''
    # endregion

    ret_dict = {}
    if observation:
        # Observation data
        ret_dict['id'] = observation.id
        ret_dict['time'] = observation.effectiveDateTime.isostring
        # Wound data
        if observation.code.coding[0].code == '72300-7':
            ret_dict['injury'] = observation.valueCodeableConcept.text
            ret_dict['bodyPart'] = observation.bodySite.text
            ret_dict['severity'] = get_severity(observation)
        # Systems injury data
        else:
            ret_dict['system'] = observation.code.text
            if ret_dict['system'] == 'Glasgow coma score total':
                ret_dict['value'] = get_GCS_score(observation)
            elif ret_dict['system'] == 'Smoke inhalation injury':
                ret_dict['value'] = ''
            elif ret_dict['system'] == 'Procedure estimated blood loss':
                ret_dict['value'] = observation.valueString

    return ret_dict


def get_encounter_id(patientID, smart) -> str:
    """
    Return the reference for the patient's triage Encounter.

    :param str patientID: The patient's FHIR ID.
    :param client.FHIRClient smart: The FHIR client.
    :return: Reference of the Encounter (e.g. 'Encounter/12345').
    """
    # Get the most recent ER admission encounter (this should be created when a patient is first admitted)
    search = enc.Encounter.where(struct={'subject': 'Patient/' + patientID,
                                         'type': '50849002',    # SNOMED code for ER admission
                                         '_sort': '-date',      # Sort the encounters newest-oldest
                                         '_count': '1'})        # Look at only the most recent encounter
    results: List[enc.Encounter] = search.perform_resources(smart.server)

    if len(results) > 0:
        return 'Encounter/' + results[0].id
    return ''


def get_current_time() -> str:
    """
    Return the current time as an ISO formatted string.

    :returns: The current time.
    """
    return datetime.now().astimezone().isoformat()

# endregion


# region TEMP CODE

def TEST_create_encounter(smart):
    from fhirclient.models.encounter import Encounter
    from fhirclient.models.encounter import EncounterParticipant
    from fhirclient.models.coding import Coding
    from fhirclient.models.codeableconcept import CodeableConcept
    from fhirclient.models.fhirreference import FHIRReference
    from fhirclient.models.period import Period
    encounter = Encounter()
    # Status of the patient, like if they have arrived or been triaged (this will change as time goes on)
    encounter.status = 'triaged'
    # Where the encounter takes place, like in the ER or in the field
    coding = Coding(
        {'system': 'http://terminology.hl7.org/CodeSystem/v3-ActCode', 'code': 'EMER', 'display': 'emergency'})
    encounter.class_fhir = coding
    # The patient being seen
    encounter.subject = FHIRReference({'reference': 'Patient/326b4675-0bc8-4dbd-b406-a5564c282401'})
    # The practitioner seeing the patient (this may change as time goes on, and I think should be empty when the patient first arrives)
    participant = EncounterParticipant()
    participant.individual = FHIRReference({'reference': 'Practitioner/03dfaa2f-a54b-4acf-bd54-80defef6ed51'})
    encounter.participant = [participant]
    # Why the patient came in (I think this should always be for Emergency room admission for this project)
    concept = CodeableConcept()
    coding = Coding(
        {'system': 'http://snomed.info/sct', 'code': '50849002', 'display': 'Emergency room admission (procedure)'})
    concept.coding = [coding]
    concept.text = 'Emergency room admission (procedure)'
    encounter.type = [concept]
    # When the encounter started and ended (times should be in ISO format)
    encounter.period = Period({'start': datetime.now().astimezone().isoformat()})
    # Which hospital the encounter took place in
    encounter.serviceProvider = FHIRReference({'reference': 'Organization/d5117822-5756-389d-9547-891a372d580f'})

    # Create the encounter on the server and get the ID
    status = encounter.create(smart.server)
    if status is not None:
        return status['id']
    return 'ERR'

# endregion

