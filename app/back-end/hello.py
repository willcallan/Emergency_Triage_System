from flask import Flask
from fhirclient import client
import fhirclient.models.patient as pat
import socket

app = Flask(__name__)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
app.config['SERVER_NAME']= IPAddr + ":5000"

settings = {
    'app_id': 'NewHat_Triage_Program',  # TODO: Come up with name?
    'api_base': 'https://r4.smarthealthit.org'
}


@app.route("/fhir")
def hello_fhir():
    smart = client.FHIRClient(settings=settings)
    patient = pat.Patient.read('d0190651-b9b0-4513-8f3b-d542319220d1',smart.server)
    return smart.human_name(patient.name[0])


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
