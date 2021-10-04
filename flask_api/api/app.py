import uuid

from flask import Flask, request
from google.cloud import dialogflow

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/detect-intent", methods=["POST"])
def detect_intent():
    if request.method == "POST":
        return "post"
    else:
        return "invalid request"


@app.route("/test-detect-intent")
def test_detect_intent():
    project_id = "chess-master-andy-mhyo"
    session_id = uuid.uuid4()
    texts = ["Hey Andy, let's play a game."]
    language_code = "en-us"
    return detect_intent_texts(project_id, session_id, texts, language_code)


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(
            response.query_result.fulfillment_text))
        return "Fulfillment text: {}\n".format(response.query_result.fulfillment_text)
