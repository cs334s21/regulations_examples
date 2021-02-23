
import os
import dotenv
import requests
import pprint

# Load the dotenv file into environment variables
dotenv.load_dotenv()
token = os.getenv('API_TOKEN')

hostname = 'https://api.regulations.gov/'
endpoint = 'v4/documents'
url = hostname + endpoint


def get_docket_doc_ids(docketId):
    params = {'filter[searchTerm]': docketId,
              'api_key': token
              }
    return requests.get(url, params=params)


if __name__ == '__main__':
    result = get_docket_doc_ids('USCG-2009-0362')

    data = result.json()
    pprint.pprint(data)

