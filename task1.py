import requests
import dotenv
import os

dotenv.load_dotenv()
token = os.getenv('API_TOKEN')


host = 'https://api.regulations.gov/'
endpoint = 'v4/documents'
url = host + endpoint

'''prints all document IDs for a given docketID'''
def printDocumentIDsInDocket(docketID):
    params = {'filter[searchTerm]':docketID, 'api_key':token}
    response = requests.get(url, params=params)

    data = response.json()
    for docs in data['data']:
        print(docs['id'])

printDocumentIDsInDocket("FWS-HQ-MB-2018-0090")