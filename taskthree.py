
import os
import dotenv
import requests

# Load the dotenv file into environment variables
dotenv.load_dotenv()
token = os.getenv('API_TOKEN')

hostname = 'https://api.regulations.gov/'
endpoint = 'v4/documents'

docketId = 'EPA-HQ-OAR-2003-0129'
url = hostname + endpoint
params = {'api_key': token,
          'filter[docketId]' : docketId}

result = requests.get(url, params=params)

data = result.json()
print('Document IDs for',docketId+':')
for item in data['data']:
    print('\t'+item['id'])
