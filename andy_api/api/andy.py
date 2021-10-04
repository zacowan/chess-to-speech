import uuid

from google.cloud import dialogflow

PROJECT_ID = "chess-master-andy-mhyo"
LANGUAGE_CODE = "en-US"


def create_session():
    # TODO: create a section in a database to store logs for the session
    # TODO: move this to a new file with the logging functions
    session_id = uuid.uuid4()
    response = {
        "ID": str(session_id)
    }
    return response


def fetch_response(session_id, text):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(PROJECT_ID, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(
        text=text, language_code=LANGUAGE_CODE)

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

    # TODO: change to audio instead of text
    return {
        "audioResponse": response.query_result.fulfillment_text
    }
