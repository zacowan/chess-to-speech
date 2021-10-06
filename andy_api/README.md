# Andy API

This API will be used to communicate with Andy.

## Getting Started

### Getting Python Set Up

1. Make sure you have Python version 3.9 installed.
2. Install pipenv by following the instructions (here)[https://pipenv.pypa.io/en/latest/install/#pragmatic-installation-of-pipenv].
3. Inside of the project directory, run `pipenv install`. This will install the required packages specified in `Pipfile`.

### Give the Proper Permissions to the Run Script

> Note: this section assumes a Mac/Linux environment. For windows instructions, do the equivalent actions.

1. Run `chmod +x run_dev.sh` to get the right privledges for using a script to run the app.

### Getting Google Cloud SDK Set Up

Follow the instructions for setting up the Google Cloud SDK locally on your computer here: https://cloud.google.com/sdk/docs/install.

### Getting the Account Service Key Set Up

Getting access to the Dialogflow API requries the use of a service account. To access a service account from our application, we need to set an environment variable with the **secret** key associated with the service account.

> For access to the key, check Discord. For detailed instructions on setting the key, see https://cloud.google.com/docs/authentication/production#passing_variable.

1. Make sure you have completed (Getting Google Cloud SDK Set Up)[#getting-google-cloud-sdk-set-up].
2. Make sure you have a key for the service account. Name it `service_key_file.json` and make sure it is somewhere easily accessible (like the root directory of this project). You will need to know the **absolute** path of the key file. Make sure that this file is correctly hidden by the `.gitignore`.
3. Update the path of the key file using the `ABSOLUTE_PATH_TO_KEY` variable in `run_dev.sh`.
4. Run the command `gcloud auth activate-service-account --key-file=ABSOLUTE_PATH_TO_KEY_FILE` using the **absolute** path of the key file (the same one set in `run.sh`).

## Running the App

1. Make sure you have completed [Getting Started](#getting-started).
2. To open a shell for the python virtual environment, run `pipenv shell` inside of the project directory.
3. While in the python virtual environment, run `./run_dev.sh` to run a script that starts the app.
4. To stop the app, use `ctrl + c`. To exit the virtual environment, type `exit`.

> Note: for a shortcut command that runs the python virtual environment shell and runs the scripts, run `pipenv run ./run_dev.sh`.
