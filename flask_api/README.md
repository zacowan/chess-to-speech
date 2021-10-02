# Flask API

This API will be used to communicate with Andy.

## Getting Started

### Getting Python Set Up

> Note: the following instructions assume a Mac/Linux environment. For windows isntructions, see https://flask.palletsprojects.com/en/2.0.x/installation/ and adjust the reccomended steps as necessary.

1. Make sure you have `Python@3.9.7` installed.
2. Make sure you are in the `flask_api/` directory (aka, root directory for this application).
3. Make a virtual environment by running `python -m venv venv`.
4. Active the virtual environment by running `. venv/bin/activate`.
5. Install required packages by running `pip install -r src/requirements.txt`.
6. To exit the virtual environment, type `deactivate`.

### Getting Google Cloud SDK Set Up

Follow the instructions for setting up the Google Cloud SDK locally on your computer here: https://cloud.google.com/sdk/docs/install.

### Getting the Account Service Key Set Up

Getting access to the Dialogflow API requries the use of a service account. To access a service account from our application, we need to set an environment variable with the **secret** key associated with the service account.

> For access to the key, check Discord. For detailed instructions on setting the key, see https://cloud.google.com/docs/authentication/production#passing_variable.

1. Make sure you have completed (Getting Google Cloud SDK Set Up)[#getting-google-cloud-sdk-set-up].
2. Make sure you have a key for the service account. Name it `service_key_file.json` and make sure it is somewhere easily accessible (like the root directory of this project). You will need to know the **absolute** path of the key file. Make sure that this file is correctly hidden by the `.gitignore`.
3. Update the path of the key file using the `ABSOLUTE_PATH_TO_KEY` variable in `run.sh`.
4. Run `chmod +x run.sh` to get the right privledges for `run.sh`.
5. Run the command `gcloud auth activate-service-account --key-file=ABSOLUTE_PATH_TO_KEY_FILE` using the **absolute** path of the key file (the same one set in `run.sh`).

## Running the App

> Note: more more detailed instructions, see https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application.

1. Make sure you have completed [Getting Started](#getting-started).
2. Make sure you are in the virtual environment by running `. venv/bin/activate` (adjust as necessary if not on Mac/Linux).
3. Run the command `./run.sh` to run the app.
4. To stop the app, use `ctrl + c`. To exit the virtual environment, type `deactivate`.
