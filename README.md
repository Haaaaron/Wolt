# Wolt internship assignment

## Quick start

### Setting up environment:

Create python3 environment in root folder.

    python3 -m venv env

Activate environment.

    source env/bin/activate

Install dependencies using requirements.txt.

    pip install -r requirements.txt

### Running in production mode:

Run commands from here on out in /backend directory

Export app and run.

    export FLASK_APP='app.py'
    flask run

Open the given url in your (default):

    http://127.0.0.1:5000/

Note that production mode is set as default for FLASK_ENV.

(On Windows, use set instead of export.)

## Running in development mode:

    export FLASK_ENV=development
    flask run

or running app.py directly.

    python3 app.py

## Environment variables:

Environment variables can be set with flask run.

    flask run --host=0.0.0.0 --port=80

Or by running app.py direclty

    PORT='5000' HOST='127.0.0.1' python3 app.py

## Testing

Run all tests with output in tests directory

    python3 -m unittest -v
