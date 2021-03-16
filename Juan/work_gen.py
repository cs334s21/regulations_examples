import random
import time
import redis
from utility_functions import\
    get_key, write_all_agencies_ids_to_file,\
    write_all_docketsIDs_in_agency_to_file,\
    write_all_documentsIDs_in_docket_to_file,\
    write_all_commentsIDs_in_document_to_file

    

def generate_jobs(database, start_key=None):
    if start_key is None:
        start_key = random.randint(0, 10)
    for _ in range(10):
        value = random.randint(0, 10)
        print(f"I am generating work {start_key} with value {value}!")
        database.hset("jobs_waiting", start_key, value)
        start_key += 1


def emulate_job_creation(database):
    for current_key in range(1, 50, 10):
        generate_jobs(database, current_key)
        time.sleep(30)

def job_creation():
    key = get_key()
    write_all_agencies_ids_to_file(key)
    with open("all_agencies_ids.txt", 'r') as r:
        for agency in r.readlines():
            agency = agency.strip()
            write_all_docketsIDs_in_agency_to_file(key, agency)
            with open("docketsIDs_in_" + agency + ".txt", 'r') as r1:
                for docket in r1.readlines():
                    docket = docket.strip()
                    write_all_documentsIDs_in_docket_to_file(key, docket)
                    with open("documentsIDS_in_" + docket + ".txt", 'r') as r2:
                        for document in r2.readlines():
                            write_all_commentsIDs_in_document_to_file(key, document.strip()) 


if __name__ == "__main__":
    # redis = redis.Redis()
    # try:
    #     redis.ping()
    #     print('Successfully connected to redis')
    #     emulate_job_creation(redis)
    # except redis.exceptions.ConnectionError as r_con_error:
    #     print('Redis connection error:', r_con_error)
    job_creation()