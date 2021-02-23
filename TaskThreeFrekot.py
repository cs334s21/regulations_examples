import requests
import os
import dotenv


# Load the dotenv file into environment variables
dotenv.load_dotenv()
token = os.getenv('API_TOKEN')

endpoint = 'v4/documents'
url = 'https://api.regulations.gov/' + endpoint + '?'

payload = {'api_key': token, 'filter[docketId]': 'EOIR-2019-0002'}

result = requests.get(url, params=payload)
jsonData = result.json()

Count = 0
for items in json['data']:
 if items['id'] != '':
     print(items['id'])
     Count += 1

print('\n' + 'Document Ids: ' + str(Count))
