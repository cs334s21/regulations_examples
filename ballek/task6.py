import os
import dotenv
import requests

# Load the dotenv file into environment variables
dotenv.load_dotenv()
token = os.getenv('API_TOKEN')

hostname = 'https://api.regulations.gov/'
endpoint = 'v4/dockets'

url = hostname + endpoint

params = {'api_key': token}

result = requests.get(url, params=params)

data = result.json()

meta = data['meta']

aggregations = meta['aggregations']

for agency in aggregations['agencyId']:
    print(agency)
