import os
import dotenv
import requests

# Load the dotenv file into environment variables
dotenv.load_dotenv()
token = os.getenv('API_TOKEN')

hostname = 'https://api.regulations.gov/'
endpoint = 'v4/documents'
document_id = "USCG-2011-1014-0002"

url = hostname + endpoint + "/" + document_id


params = {
          'api_key': token
          }


result = requests.get(url, params)

data = result.json()

# Files are kept track of in the document's attachments
attachments = data["data"]["relationships"]["attachments"]["links"]

# This loop shows all the different groups of attachments
# It appears that ["related"] is what it's important but I'll leave the loop here
# for attachment_type in attachments.keys():
#     print(attachment_type)
#     attachment_result = requests.get(attachments[attachment_type], params)
#     print(attachment_result.json())
#     print()

attachment_url = attachments["related"]
attachment_data = requests.get(attachment_url, params).json()

for file_format in attachment_data["data"][0]["attributes"]["fileFormats"]:
    file_url = file_format["fileUrl"]
    file_name = file_url.split("/")[-1]

    file_dl = requests.get(file_url, allow_redirects=True)
    with open(file_name, "wb") as downloaded_file:
        downloaded_file.write(file_dl.content)
