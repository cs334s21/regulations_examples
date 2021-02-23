import requests
import os
import dotenv


# Load the dotenv file into environment variables
dotenv.load_dotenv()
token = os.getenv('API_TOKEN')

endpoint = 'v4/documents'
url = 'https://api.regulations.gov/' + endpoint + '?'

payload = {'api_key': token, 'filter[docketId]': 'EOIR-2020-0003'}

result = requests.get(url, params=payload)
jsonData = result.json()

idCounter = 0
for item in jsonData['data']:
    if item['id'] != '':
        print(item['id'])
        idCounter += 1
    
print('\n' + 'Number of Document Ids: ' + str(idCounter))


