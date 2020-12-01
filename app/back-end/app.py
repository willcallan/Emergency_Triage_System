from flask import Flask
from flasgger import Swagger
import socket
from flask_cors import CORS, cross_origin
from dataGenerator import DataGenerator
import os
# Import routes
from hello import hello_world
from practitioner import practitioner_endpoint
from patient import patient_endpoint
from observation import observation_endpoint


app = Flask(__name__)
app.config.from_pyfile('vars.py')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/generate")
def hello():
    gen = DataGenerator()
    gen.generate_patients(25)
    gen.generate_practitioners(10)

    return "LOADED DEMO DATA"


# Route registration
app.register_blueprint(hello_world)
app.register_blueprint(patient_endpoint)
app.register_blueprint(practitioner_endpoint)
app.register_blueprint(observation_endpoint)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

swagger = Swagger(app)

if bool(os.environ.get('GENERATE_DATA')):
    gen = DataGenerator()
    gen.generate_patients(25)
    gen.generate_practitioners(10)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
