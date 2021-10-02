from flask import Flask, request
from google.cloud.dialogflowcx_v3beta1.services.agents import AgentsClient
from google.cloud.dialogflowcx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3beta1.types import session

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/detect_intent", methods=['POST'])
def detect_intent():
    if request.method == 'POST':
        return 'post'
    else:
        return 'invalid request'
