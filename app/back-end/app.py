from flask import Flask
from flasgger import Swagger
import socket
from flask_cors import CORS, cross_origin
# Import routes
from hello import hello_world
from practitioner import practitioner_endpoint
from patient import patient_endpoint

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# Route registration
app.register_blueprint(hello_world)
app.register_blueprint(patient_endpoint)
app.register_blueprint(practitioner_endpoint)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
app.config['SERVER_NAME']= IPAddr + ":5000"

swagger = Swagger(app)

if __name__ == "__main__":
    app.run()
