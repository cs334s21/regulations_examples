import time
from json import dumps, loads
import requests
from utility_functions import \
get_dockets, get_documents, get_comments
from utility_functions import get_key


class Client:
    def __init__(self):
        self.url = "http://localhost:8080"


    def handle_error(self, j_id, data):
        while j_id == "error":
            print("I'm sleeping a minute.")
            time.sleep(60)
            j_id, j_type, ids = request_job(self.url, data)
        return j_id, j_type, ids

    def get_job(self):
        full_url = f"{self.url}/get_job"
        c_id = self.get_client_id()
        data = {"client_id": c_id}
        j_id, j_type, ids = request_job(full_url, data)
        if j_id == "error":
            j_id, j_type, ids = self.handle_error(j_id, data)
        return j_id, j_type, ids

    def send_job_results(self, j_id, job_result):
        end_point = "/put_results"
        c_id = self.get_client_id()
        data = {j_id: job_result, "client_id": c_id}
        request = requests.put(self.url + end_point, data=dumps(data))
        request.raise_for_status()

    def request_client_id(self):
        end_point = "/get_client_id"
        request = requests.get(self.url + end_point)

        # Check if status code is 200 type code: successful GET
        if request.status_code // 100 == 2:
            c_id = int(request.json()['client_id'])
            write_client_id(c_id)
            return c_id
        return -1

    # Reads from file, or requests if nothing there
    def get_client_id(self):
        c_id = read_client_id()
        if c_id == -1:
            c_id = self.request_client_id()
        if c_id == -1:
            print("Could not get client ID!")
        return c_id

    def complete_client_request(self):
        j_id, j_type, ids = self.get_job()
        results = perform_job(j_id, j_type, ids)
        self.send_job_results(j_id, results)


# Helper functions (don't need to be a part of the class)
def request_job(full_url, data):
    request = requests.get(full_url, data=dumps(data))
    #if status code is 400 client will handle it
    if request.status_code != 400:
        request.raise_for_status()
    work_id, j_type, ids = list(loads(request.text).items())[0]
    return work_id, j_type, ids


def perform_job(j_id, j_type, ids):
    results = []
    key = get_key()
    if j_type == 'dockets':
        get_dockets(key, ids,results)
    elif j_type == 'documents':
        get_documents(key, ids,results)
    elif j_type == 'comments':
        get_comments(key, ids,results) 

    return results



def read_client_id():
    try:
        with open("client.cfg", "r") as file:
            return int(file.readline())
    except FileNotFoundError:
        return -1


def write_client_id(c_id):
    with open("client.cfg", "w") as file:
        file.write(str(c_id))


if __name__ == "__main__":
    client = Client()
    client_id = client.get_client_id()
    print("ID of this client: ", client_id)

    while True:
        client.complete_client_request()
