# Wolt internship assignment

## Setting up environment:

Create python3 environment in root folder:

    python3 -m venv env

Activate environment:

    source env/bin/activate

Install dependencies using requirements.txt:

    pip install -r requirements.txt

## Running in production mode:

Run commands from here on out in /backend directory

Export app and run:

    export FLASK_APP='app.py'
    flask run

Open the given url in your browser (default):

    http://127.0.0.1:5000/

Note that production mode is set as default for FLASK_ENV

(On Windows, use set instead of export.)

### Endpoints

GET /discovery Query params:
  - lat: float
  - lon: float

Example:

Get

    curl "http://127.0.0.1:5000/discovery?lat=60.1709&lon=24.941"

Response (Long list of restaurants)

```
{
  "sections": [
    {
      "title": "Popular restaurants", 
      "restaurants": [
        {
          "blurhash": "UAN=8k?LS~M:ErJFs%t0MDMWRqo@%BxSV{RX", 
          "launch_date": "2020-04-20", 
          "location": [
            24.938082, 
            60.17626
          ], 
          "name": "Sea Chain", 
          "online": true, 
          "popularity": 0.9569904141
        }, 
        {
          "blurhash": "UKB;Mk]|I^oJ1SJD$ebHESNMj[a}-4xBNeWX", 
          "launch_date": "2020-10-25", 
          "location": [
            24.949733, 
            60.166172
          ], 
          "name": "Bacon Basket", 
          "online": true, 
          "popularity": 0.9482709721
        }, ...
``` 

Example error

Get

    curl "http://0.0.0.0:5000/discovery?lat=&lon="

```
{
  "error": "'lat'=='' and/or 'lon'=='' query parameters unspecified"
}
```

## Running in development mode:

    export FLASK_ENV=development
    flask run

or running app.py directly:

    python3 app.py

## Environment variables:

Environment variables can be set with flask run:

    flask run --host=0.0.0.0 --port=80

Or by running app.py direclty:

    PORT='5000' HOST='127.0.0.1' python3 app.py

## Testing

Run all tests with output in tests directory:

    python3 -m unittest -v
