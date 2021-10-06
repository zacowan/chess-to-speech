import uuid

from google.cloud import speech, storage

BUCKET_NAME = "chess-to-speech"
FILENAME_PREFIX = "audio-files/"
FILE_TYPE = "audio/webm"
FILE_SAMPLE_RATE = 48000


def upload_audio_file(file_to_upload):
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob_name = FILENAME_PREFIX + str(uuid.uuid4())
        blob = bucket.blob(blob_name)

        blob.upload_from_string(file_to_upload, content_type=FILE_TYPE)

        return blob_name
    except Exception as e:
        print(e)
        return None


def transcribe_audio_file(file_to_transcribe):
    try:
        client = speech.SpeechClient()

        file_name = upload_audio_file(file_to_transcribe)

        if file_name == None:
            raise Exception("File name returned None")

        gcs_uri = "gs://" + BUCKET_NAME + "/" + file_name

        audio = speech.RecognitionAudio(uri=gcs_uri)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
            sample_rate_hertz=FILE_SAMPLE_RATE,
            language_code="en-US"
        )

        response = client.recognize(config=config, audio=audio)

        # for result in response.results:
        #     print("Transcript: {}".format(result.alternatives[0].transcript))

        return response.results[0].alternatives[0].transcript
    except Exception as e:
        print(e)
        return None
