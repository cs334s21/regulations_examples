
import os
import dotenv
import requests

# Load the dotenv file into environment variables
dotenv.load_dotenv()
token = os.getenv('API_TOKEN')

hostname = 'https://api.regulations.gov/'
endpoint = 'v4/documents'

url = hostname + endpoint

params = {'filter[searchTerm]': 'water',
          'api_key': token
          }

result = requests.get(url, params=params)

data = result.json()

print(data)
