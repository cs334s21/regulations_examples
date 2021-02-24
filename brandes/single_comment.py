import os
import dotenv
import requests

# Load the dotenv file into environment variables
dotenv.load_dotenv()
token = os.getenv('API_TOKEN')

hostname = 'https://api.regulations.gov/'
endpoint = 'v4/comments'
document_id = "FMCSA-1997-2350-2476"

url = hostname + endpoint + "/" + document_id


params = {
          'api_key': token
          }


result = requests.get(url, params)

data = result.json()

# Files are kept track of in the document's attachments
attachments = data["data"]["relationships"]["attachments"]["links"]

attachment_url = attachments["related"]
attachment_data = requests.get(attachment_url, params).json()

for file_format in attachment_data["data"][0]["attributes"]["fileFormats"]:
    file_url = file_format["fileUrl"]
    file_name = file_url.split("/")[-1]

    file_dl = requests.get(file_url, allow_redirects=True)
    with open(file_name, "wb") as downloaded_file:
        downloaded_file.write(file_dl.content)
