import requests
import query_options
import dotenv, os, sys
import time
from bs4 import BeautifulSoup
from date_formatting import  clean_date, to_eastern_time


"""general purpose functions"""

def comment_count_in_text_file(output):
    with open(output, 'r') as reader:
        text = reader.read()
        return text.count(' "id" ')
      
def get_key():
    dotenv.load_dotenv()
    return os.getenv('API_TOKEN')

def get_umf():
    """return upper most folder"""
    return "regulation_database_items_ids"

"""helper functions to list child objects using a parentItemId"""

def write_all_items_in_parentItem_to_a_file(output, url, params):
    """
    Args:
        total_elements (int): total numbers of items in parentItem
        output (string): name of desire output file
        url (url): full path to one of these 
            end points [comments, documents, dockets]
        params (dict): dict with parameter to filter by
            documentID, docketID, or agencyID.
            a.k.a. parentID
    """
    total_elements = get_total_elements_in_parentItem(url, params)
    try:
        with open(output, 'w') as writer:
            while(total_elements > 0):
                print(f"{url[31:]} left to write: {total_elements}")
                for page in range(1, 21):
                        query_options.update_page(page, params)
                        r = request_but_sleep_if_429(url, params)
                        r.raise_for_status()
                        write_page_of_items_to_file( r, writer, params)
                update_next_lastModifiedDate(url, params)
                total_elements -= 5000
    except IndexError:
        print("ran out of items to download")

def write_page_of_items_to_file(request_, writer, params):
    writer.write(beautify_text(request_.text))

def beautify_text(text):
    return BeautifulSoup(text, "html.parser").text


"""helper functions to write childIDs using parentID."""
      
def write_all_itemsIDs_in_parentItem_to_file(output, url, params):
    total_elements = get_total_elements_in_parentItem(url, params)
    try:
        with open(output, 'w') as writer:
            while(total_elements > 0):
                print(f"{url[31:]} left to write: {total_elements}")
                for page in range(1, 21):
                    items = get_items(url, page, params)
                    write_page_of_ids_to_file(items, writer)
                update_next_lastModifiedDate(url, params)
                total_elements -= 5000
    except IndexError:
        print("ran out of items to download")

def write_page_of_ids_to_file(items, writer):
    for item in items['data']:
        writer.write(f"{item['id']}\n")


"""helper functions to write childIDs using parentObjectID.
this functions apply for the relationship between:
documents and comments"""

def write_all_objectsIDs_in_parentItem_to_file(output, url, params):
    total_elements = get_total_elements_in_parentItem(url, params)
    try:
        write_all_objectsIDs_to_file(total_elements, output, url, params)
    except IndexError:
        print("ran out of items to download")

def write_all_objectsIDs_to_file(total_elements, output, url, params):
    with open(output, 'w') as writer:
        while(total_elements > 0):
            print(f"{url[31:]} left to write: {total_elements}")
            write_20_pages_of_objectsIDs_to_file(url, writer, params)
            total_elements -= 5000

def write_20_pages_of_objectsIDs_to_file(url, writer, params):
    for page in range(1, 21):
        items = get_items(url, page, params)
        for item in items['data']:
            writer.write(item["attributes"]["objectId"] + '\n')
    update_next_lastModifiedDate(url, params)


"""helper functions for the write-to-file above functions"""

def get_items(url, page, params):
    query_options.update_page(page, params)
    r = request_but_sleep_if_429(url, params)
    return r.json()

def request_but_sleep_if_429(url, params):
    r = request_from_reg_api(url, params)
    if r.status_code == 429:
        print("Finished with 1000 calls")
        print("I gonna nap an hour. bye, bye")
        time.sleep(3600)
        print("Hey, I am back to work!!")
        r = request_from_reg_api(url, params)
    r.raise_for_status()
    return r

def request_from_reg_api(end_point, params):
    return requests.get(end_point, params=params)

def get_total_elements_in_parentItem(url, params):
    """expects url pointing to a list of comments, dockets, or docs.
    params should filter data by one parent item ID.\n
    ex. params dict contains filter["documentId"]:value 
    when querying for comments.
    """
    results = request_but_sleep_if_429(url, params=params)
    results.raise_for_status()
    return int(results.json()['meta']['totalElements'])

def update_next_lastModifiedDate(url, params):
    r = request_but_sleep_if_429(url, params)
    r.raise_for_status()
    params["filter[lastModifiedDate][ge]"] =\
    to_eastern_time(clean_date(get_next_lastModifiedDate(r)))

def get_next_lastModifiedDate(request_):
    """
    expects a request obj to regulationsAPI with a json containing
    a list of dockets, docs, or comments.
    """
    return request_.json()['data'][-1]['attributes']['lastModifiedDate']

def set_parent_ID(default_parentID):
    try:
        return  sys.argv[1]
    except IndexError:
        if default_parentID is not None:
            return default_parentID
        raise IndexError("Need to provide parentID")

def set_initial_params(KEY, params):
    """set often used key-value pair in params"""
    query_options.add_key_to_params(KEY, params)
    query_options.sort_by_last_modified_date(params)
    query_options.set_page_size(250, params)



"""agency functions """

def write_all_agencies_ids_to_file(key):
    """returns a list of all agency ID's.
    """
    url = docket_url()
    params = {}
    data = get_agencies_from_docket_meta_data(key, url, params)
    write_agencies_to_file(data)

def get_agencies_from_docket_meta_data(key, url, params):
    query_options.add_key_to_params(key, params)
    result = request_but_sleep_if_429(url, params=params)
    result.raise_for_status()
    return result.json()

def write_agencies_to_file(data):
    agencies = data['meta']['aggregations']['agencyId']
    with open(f'{get_umf()}/all_agencies_ids.txt', 'w') as w:
        for agency in agencies:
            w.write(f"{agency['value']}\n")


"""docket functions"""

def docket_url():
    return 'https://api.regulations.gov/v4/dockets'

def write_all_dockets_in_agency_to_file(key, agency_dir, agency_id=None):
    agencyID, params = get_agencyID_and_params(key, agency_id)
    output = f"{agency_dir}/{agency_id}/docketsIDs_in_{agencyID}.txt"
    write_all_items_in_parentItem_to_a_file(output, docket_url(), params)

def write_all_docketsIDs_in_agency_to_file(key, agency_dir, agency_id=None):
    agencyID, params = get_agencyID_and_params(key, agency_id)
    output = f"{agency_dir}/docketsIDs_in_{agencyID}.txt"
    write_all_itemsIDs_in_parentItem_to_file(output, docket_url(), params)

def get_agencyID_and_params(key, agency_id):
    agencyID = set_parent_ID(agency_id)
    params = {}
    set_up_docket_query_params(key, agencyID, params)
    return agencyID, params

def set_up_docket_query_params(key, agencyID, params):
    set_initial_params(key, params)
    query_options.filter_by_agencyID(agencyID, params)

def get_docket_details(key, docket_id):
    params = {}
    query_options.add_key_to_params(key, params)
    docket_location = f"{docket_url()}/{docket_id}"
    result = request_but_sleep_if_429(docket_location, params=params)
    result.raise_for_status()
    return result.json()


def get_dockets(key, docket_ids, results):
    for docket_id in docket_ids:
        results.append(get_docket_details(key, docket_id))


"""document functions"""

def document_url():
    return 'https://api.regulations.gov/v4/documents'


def write_all_documents_in_docket_to_file(key, output, docket_id=None):

    docketID, params = get_docketID_and_params(key, docket_id)
    output = f"{output}/documents_in_{docketID}.txt"
    write_all_items_in_parentItem_to_a_file(output, document_url(), params)

def write_all_documentsIDs_in_docket_to_file(key, output, docket_id=None):

    docketID, params = get_docketID_and_params(key, docket_id)
    output1 = f"{output}/documentsIDs_in_{docketID}.txt"
    write_all_itemsIDs_in_parentItem_to_file(output1, document_url(), params)
    output2 = f"{output}/documentsObjectIDs_in_{docketID}.txt"
    write_all_objectsIDs_in_parentItem_to_file(output2, document_url(), params)

def get_docketID_and_params(key, docket_id):
    docketID = set_parent_ID(docket_id)
    params = {}
    set_up_document_query_params(key, docketID, params)
    return docketID, params

def set_up_document_query_params(key, docketID, params):
    set_initial_params(key, params)
    query_options.filter_by_docketID(docketID, params)

def get_document_details(key, document_id):
    params = {}
    query_options.add_key_to_params(key, params)
    document_location = f"{document_url()}/{document_id}"
    result = request_but_sleep_if_429(document_location, params=params)
    result.raise_for_status()
    return result.json()

def get_documents(key, document_ids, results):
    for document_id in document_ids:
        results.append(get_document_details(key, document_id))


"""comments functions"""

def comment_url():
    return 'https://api.regulations.gov/v4/comments'

def write_all_comments_in_document_to_file(key, document_dir, document_id=None):
    documentID, params = get_documentID_and_params(key, document_id)
    output = f"{document_dir}/comments_in_{documentID}.txt"
    write_all_items_in_parentItem_to_a_file(output, comment_url(), params)

def write_all_commentsIDs_in_document_to_file(key, document_dir, document_id=None):
    documentID, params = get_documentID_and_params(key, document_id)
    output = f"{document_dir}/commentsIDs_in_{documentID}.txt"
    write_all_itemsIDs_in_parentItem_to_file(output, comment_url(), params)

def get_documentID_and_params(key, document_id):
    documentID = set_parent_ID(document_id)
    params = {}
    set_up_comment_query_params(key, documentID, params)
    return documentID, params

def set_up_comment_query_params(key, documentID, params):
    set_initial_params(key, params)
    query_options.filter_by_documentID(documentID, params)

def get_comment_details(key, comment_id):
    params = {}
    query_options.add_key_to_params(key, params)
    comment_location = f"{comment_url()}/{comment_id}"
    result = request_but_sleep_if_429(comment_location, params=params)
    result.raise_for_status()
    return result.json()


def get_comments(key, comment_ids, results):
    for comment_id in comment_ids:
        results.append(get_comment_details(key, comment_id))


