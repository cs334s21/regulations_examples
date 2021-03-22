import requests

def update_page(page_number, params): 
    params["page[number]"] = str(page_number)

def set_page_size(page_size, params):
    params["page[size]"] = str(page_size)

def add_key_to_params(key, params):
    params.update({   
        "api_key": key
    })

def add_sort(value, params):
    try:
        params["sort"] = params["sort"] + value
    except KeyError:
        params["sort"] = value

def sort_by_posted_date(params):
    add_sort("postedDate", params)

def sort_by_last_modified_date(params):
    add_sort("lastModifiedDate", params)

def sort_by_documentID(params):
    add_sort("documentId", params)

def filter_by_agencyID(agencyID, params): 
    params["filter[agencyId]"] = agencyID

def filter_by_term(term, params):
    params["filter[searchTerm]"] = term
    
def filter_by_posted_date(date, params):
    params["filter[postedDate]"] = date

def filter_by_ge_posted_date(date, params):
    params["filter[postedDate][ge]"] = date

def filter_by_le_posted_date(date, params):
    params["filter[postedDate][le]"] = date

def filter_by_last_modified(dateTime, params):
    params["filter[lastModifiedDate]"] = dateTime

def filter_by_ge_last_modified(dateTime, params):
    params["filter[lastModifiedDate][ge]"] = dateTime

def filter_by_le_last_modified(dateTime, params):
    params["filter[lastModifiedDate][le]"] = dateTime

def filter_by_documentID(documentID, params):
    params["filter[commentOnId]"] = documentID

def filter_by_docketID(docketID, params):
    params["filter[docketId]"] = docketID
