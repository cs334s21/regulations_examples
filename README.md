# regulations_examples

## Setup

* Create a virtual environment

 `python3 -m venv .venv`
 
* Activate the virtual environment

 `source .venv.bin/activate`
 
* Install the project requirements

 `pip install -r requirements.txt`
 
* Create a `.env` file containing a key

 ```
 API_TOKEN=<insert key here>
 ```

See `coleman/download.py` for an example of how to read the `.env` file using
the `python-dotenv` library (installed via `requirements.txt`).


The `.gitignore` is set to ignore the `.env` file.  DO NOT add this file 
to the repo because it contains you API key!!!
 