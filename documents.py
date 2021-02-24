import os
from dotenv import load_dotenv
import requests


load_dotenv()
api_key = os.getenv('API_TOKEN')

hostname = 'https://api.regulations.gov/'
endpoint = 'v4/documents'
url = hostname + endpoint


def print_documents(documents):
    document_num = 0
    for document in documents:
        print(document_num:=document_num+1, document, '\n')


def get_documents_from_docket_id(docket_id):
    params = {'filter[docketId]' : docket_id, 'api_key' : api_key}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['data']


def main():
    docket_id = 'EPA-HQ-OAR-2003-0129'
    documents = get_documents_from_docket_id(docket_id)
    print_documents(documents)


if __name__ == '__main__':
    main()
