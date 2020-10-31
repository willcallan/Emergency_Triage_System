from flask import Blueprint
from fhirclient import client
import fhirclient.models.patient as pat
from vars import settings
from flasgger.utils import swag_from

hello_world = Blueprint('hello_world',__name__)


@hello_world.route("/fhir")
@swag_from('static/hello_world_fhir.yml')
def hello_fhir():
    smart = client.FHIRClient(settings=settings)
    patient = pat.Patient.read('d0190651-b9b0-4513-8f3b-d542319220d1',smart.server)
    return smart.human_name(patient.name[0])


@hello_world.route("/")
@swag_from('static/hello_world.yml')
def hello():
    return "Hello World!"
