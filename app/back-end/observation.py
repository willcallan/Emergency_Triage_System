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

from vars import settings, body_site_lookup, injury_lookup

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
    search_params['subject'] = 'Patient/' + patient_id
    search_params['encounter'] = get_encounter_id(patient_id, smart)

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

    :param dict data: The input data as a JSON dict:
            {patientID: '',
            bodyPart: '',
            injury: '',
            severity: '' OPTIONAL}
    :param client.FHIRClient smart: The FHIR client.
    :return: Observation resource.
    """

    # region Nested Functions
    def get_current_time() -> str:
        """
        Return the current time as an ISO formatted string.

        :returns: The current time.
        """
        return datetime.now().astimezone().isoformat()

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
        wound_data = injury_lookup[term]
        concept = CodeableConcept()
        concept.coding = [Coding({'system': 'http://loinc.org', 'code': wound_data[0], 'display': wound_data[1]})]
        concept.text = concept.coding[0].display
        return concept
    # endregion

    observation = obs.Observation()
    # Status of the observation (specific values found at https://www.hl7.org/fhir/codesystem-observation-status.html)
    observation.status = 'preliminary'
    # How the observation was conducted
    categoryconcept = CodeableConcept()
    categoryconcept.coding = [Coding({'system': 'http://terminology.hl7.org/CodeSystem/observation-category', 'code': 'exam', 'display': 'exam'})]
    observation.category = [categoryconcept]
    # Marking that this observation is about a wound
    codeconcept = CodeableConcept()
    codeconcept.coding = [Coding({'system': 'http://loinc.org', 'code': '72300-7', 'display': 'Wound type'})]
    codeconcept.text = codeconcept.coding[0].display
    observation.code = codeconcept
    # The patient being observed
    observation.subject = FHIRReference({'reference': 'Patient/' + data['patientID']})
    # The encounter that this observation is part of
    observation.encounter = FHIRReference({'reference': get_encounter_id(data['patientID'], smart)})

    # The time that this observation was first made (times should be in ISO format)
    observation.effectiveDateTime = FHIRDate(get_current_time())
    # The time that this observation was reviewed and approved (times should be in ISO format)
    observation.issued = observation.effectiveDateTime
    # The body part that is marked
    observation.bodySite = get_bodysite_concept(data['bodyPart'])
    # The results of the observation (the field used for this changes depending on how the observation was measured)
    observation.valueCodeableConcept = get_wound_value_concept(data['injury'])
    # The severity of the wound
    if 'severity' in data:
        note = Annotation({'time': get_current_time(), 'text': 'Marked severity: ' + data['severity']})
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
    # endregion

    ret_dict = {}
    if observation:
        # Observation data
        ret_dict['id'] = observation.id
        # Wound data
        if observation.code.coding[0].code == '72300-7':
            ret_dict['injury'] = observation.valueCodeableConcept.text
            ret_dict['bodyPart'] = observation.bodySite.text
            ret_dict['time'] = observation.effectiveDateTime.isostring
            ret_dict['severity'] = get_severity(observation)

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

