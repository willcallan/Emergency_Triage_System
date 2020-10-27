from flask import Flask
from flasgger import Swagger
import socket

# Import routes
from hello import hello_world

app = Flask(__name__)

# Route registration
app.register_blueprint(hello_world)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
app.config['SERVER_NAME']= IPAddr + ":5000"

swagger = Swagger(app)

if __name__ == "__main__":
    app.run()
