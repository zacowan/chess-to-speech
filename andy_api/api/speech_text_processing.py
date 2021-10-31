"""This module handles the processing of audio files.

Attributes:
    BUCKET_NAME: the name of the bucket to upload user's audio to for STT.
    FILENAME_PREFIX: the directory in the bucket to store audio files for STT.
    FILE_TYPE: the type of the file to be processed for STT.
    BOARD_LOCATION_CC: the name of the BoardLocation custom class for
        STT.
    FILE_SAMPLE_RATE: the sample rate of the file to be processed for STT.
    OUTPUT_FILE_NAME: the name of the file to output for TTS.

"""
import uuid

from google.cloud import speech_v1p1beta1 as speech, storage, texttospeech

BUCKET_NAME = "chess-to-speech"
FILENAME_PREFIX = "audio-files/"
FILE_TYPE = "audio/wav"
MOVE_PIECE_PHRASE_SET = "projects/408609438071/locations/global/phraseSets/MovePiece"
FILE_SAMPLE_RATE = 48000
OUTPUT_FILE_NAME = "andy_response.wav"


def upload_audio_file(file_to_upload):
    """Uploads an audio file to gcloud storage.

    Args:
        file_to_upload (blob): the blob to upload.

    Returns:
        str: the name of the file uploaded.

    """
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob_name = FILENAME_PREFIX + str(uuid.uuid4())
        blob = bucket.blob(blob_name)

        blob.upload_from_string(file_to_upload, content_type=FILE_TYPE)

        return blob_name
    except Exception as err:
        print(err)
        raise


def generate_audio_response(text):
    """Converts text into an audio file.

    Args:
        text (str): the text to transform into audio.

    Returns:
        bytes: the audio bytes generated.

    """
    try:
        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # # The response's audio_content is binary.
        # with open(OUTPUT_FILE_NAME, "wb") as out:
        #     # Clear the contents of the file
        #     out.truncate(0)
        #     # Write the response to the output file.
        #     out.write(response.audio_content)

        return response.audio_content
    except Exception as err:
        print(err)
        raise


def transcribe_audio_file(file_to_transcribe):
    """Converts an audio file into text.

    Args:
        file_to_transcribe (blob): the blob to transcribe.

    Returns:
        text (str): the text interpreted from the audio.
        location (str): the location of the audio file in GCP.

    """
    try:
        client = speech.SpeechClient()

        file_name = upload_audio_file(file_to_transcribe)

        gcs_uri = "gs://" + BUCKET_NAME + "/" + file_name

        audio = speech.RecognitionAudio(uri=gcs_uri)

        # Model adaptation

        # Speech adaptation configuration
        speech_adaptation = speech.SpeechAdaptation(
            phrase_set_references=[MOVE_PIECE_PHRASE_SET])

        # Note: the encoding and sample_rate_hertz should change based on what
        # file is expected.
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
            sample_rate_hertz=FILE_SAMPLE_RATE,
            language_code="en-US",
            adaptation=speech_adaptation
        )

        response = client.recognize(config=config, audio=audio)

        try:
            return response.results[0].alternatives[0].transcript, gcs_uri
        except IndexError:
            return None, gcs_uri
    except Exception as err:
        print(err)
        raise
