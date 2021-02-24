import os
import dotenv
import requests

dotenv.load_dotenv()
token = os.getenv('API_TOKEN')

hostname = 'https://api.regulations.gov/'


def get_docket_documents(current_docket_id):
    endpoint = 'v4/documents'
    url = hostname + endpoint
    params = {
        'filter[docketId]': current_docket_id,
        'api_key': token
    }

    return requests.get(url, params=params).json()


def get_document_comments(object_id):
    endpoint = 'v4/comments'
    url = hostname + endpoint
    params = {
        'filter[commentOnId]': object_id,
        'api_key': token
    }

    return requests.get(url, params=params).json()


docket_id = 'FAA-2018-1084'
documents = get_docket_documents(docket_id)

print('Documents for docket {}:'.format(docket_id))

for document in documents['data']:
    document_comments = get_document_comments(document['attributes']['objectId'])
    print(' - Document {} has {} comments'.format(document['id'], document_comments['meta']['totalElements']))
