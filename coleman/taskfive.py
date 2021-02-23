# Author: Larisa Fava
# Assignemnt: Capstone Snow Day (02/22/21)
# Purpose: Find all documents in a given Docket

import os
import dotenv
import requests

# Load the dotenv file into environment variables
count = 0
dotenv.load_dotenv()
token = os.getenv('API_TOKEN')

hostname = 'https://api.regulations.gov/'
endpoint = 'v4/documents'
# docketId = 'EPA-HQ-OAR-2003-0129'
docketId = 'EOIR-2020-0003'

url = hostname + endpoint
params = {'api_key' : token,
            'filter[docketId]' : docketId}

result = requests.get(url, params=params)

data = result.json()
print('All Documents in Docket (' + docketId + '):')
print()
for document in data['data']:
    count += 1
    print('Document', count, ':')
    print(document)
    print()
