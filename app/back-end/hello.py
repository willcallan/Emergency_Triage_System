from flask import Flask
import socket

app = Flask(__name__)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
app.config['SERVER_NAME']= IPAddr + ":5000"

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
