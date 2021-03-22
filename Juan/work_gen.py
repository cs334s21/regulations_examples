import random
import time, os
from utility_functions import\
    get_key, write_all_agencies_ids_to_file,\
    write_all_docketsIDs_in_agency_to_file,\
    write_all_documentsIDs_in_docket_to_file,\
    write_all_commentsIDs_in_document_to_file,\
    get_umf

# upper most folder
umf = get_umf()

def job_creation():
    key = get_key()
    if not os.path.exists(f"./{umf}"):
        os.makedirs(umf)
    if not os.path.exists(f"./{umf}/all_agencies_ids.txt"):
        write_all_agencies_ids_to_file(key)
    with open(f"{umf}/all_agencies_ids.txt", 'r') as r:
        for agency in r.readlines():
            agency = agency.strip()
            agency_dir = f"{umf}/{agency}"
            if not os.path.exists(f"./{agency_dir}"):
                os.makedirs(agency_dir)
            if not os.path.exists(f"./{agency_dir}/docketsIDs_in_{agency}.txt"):
                write_all_docketsIDs_in_agency_to_file(key, agency_dir,  agency)
            with open(f"{umf}/{agency}/docketsIDs_in_{agency}.txt", 'r') as r1:
                for docket in r1.readlines():
                    docket = docket.strip()
                    docket_dir = f"{umf}/{agency}/{docket}" 
                    if not os.path.exists(f"./{docket_dir}"):
                        os.makedirs(docket_dir)
                    if not os.path.exists(f"./{docket_dir}/documentsIDs_in_{docket}.txt"):
                        write_all_documentsIDs_in_docket_to_file(key, docket_dir, docket)
                    with open(f"{docket_dir}/documentsIDs_in_{docket}.txt", 'r') as r2:
                        for document in r2.readlines():
                            document = document.strip()
                            document_dir = f"{docket_dir}/{document}"
                            if not os.path.exists(f"./{document_dir}"):
                                os.makedirs(document_dir)
                            if not os.path.exists(f"./{document_dir}/commentsIDs_in_{document}.txt"):
                                write_all_commentsIDs_in_document_to_file(key, document_dir, document) 


if __name__ == "__main__":
    job_creation()