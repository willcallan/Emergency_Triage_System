from flask import Blueprint, request
from datetime import datetime

from flask_cors import CORS, cross_origin
from flask import jsonify

from fhirclient import client
import fhirclient.models.observation as obs
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.fhirdate import FHIRDate

from vars import settings, body_site_lookup, injury_lookup

observation_endpoint = Blueprint('observation_endpoint', __name__)


# region URL Functions

# TODO: ask Vaneet what type of data he wants to pass and return
@observation_endpoint.route('/observation/save', methods=['POST'])
def observation_save():
    """
    Saves an observation into the FHIR server.
    """
    # Get the posted patient
    data_json = request.get_json()
    smart = client.FHIRClient(settings=settings)
    observation = populate_observation(data_json)

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
@observation_endpoint.route('/observation', methods=['GET'])
def observation_search():
    """
    Searches for all observations by patient ID, returns a list of observation dicts.
    """
    patient_id = request.args.get('id')

    # If no id is provided, return nothing
    if not patient_id:
        return ''

    # Specify the search parameters
    search_params = {
        'subject': 'Patient/' + patient_id,
        # TODO: Get the encounter ID from the database using the patient_id
        # 'encounter': 'get encounter id from db',
    }

    # Search for all observations who match the search parameters
    smart = client.FHIRClient(settings=settings)
    search = obs.Observation.where(struct=search_params)
    observations = search.perform_resources(smart.server)

    ret_list = []
    for o in observations:
        ret_list.append(get_observation_data(o, smart))

    # TODO: return a jsonified list
    return 'NEED TO IMPLEMENT'  # UNCOMMENT WHEN CODE IS VALID: jsonify(ret_list)

# endregion


# region Functions

def populate_observation(data) -> obs.Observation:
    """
    Returns an Observation resource populated with the input data.

    :param dict data: The input data as a JSON dict:
            {patientID: '',
            bodyPart: '',
            injury: ''}
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
    #TODO: We should save the patient's Encounter in the db as well, since it will hold all the triage observations
    # observation.encounter = FHIRReference({'reference': 'Encounter/ce115934-fe9d-43cf-a2e7-241d16b6d839'})

    # The time that this observation was first made (times should be in ISO format)
    observation.effectiveDateTime = FHIRDate(get_current_time())
    # The time that this observation was reviewed and approved (times should be in ISO format)
    observation.issued = observation.effectiveDateTime
    # The body part that is marked
    observation.bodySite = get_bodysite_concept(data['bodyPart'])
    # The results of the observation (the field used for this changes depending on how the observation was measured)
    observation.valueCodeableConcept = get_wound_value_concept(data['injury'])

    return observation


# TODO: Implement
def get_observation_data(observation, smart):
    return ''

# endregion
