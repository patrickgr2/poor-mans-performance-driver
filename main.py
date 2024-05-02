import httpx
import json
import random   
import time
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor
import concurrent.futures as cf

DEV_URL_FIND_USER = f"http://localhost:8080/api/v1/user/"
KEYCLOAK_URL = "https://bss-int.dev.bip.va.gov/auth/realms/csap/"
def query_users(user_count, client):
    fi = open("local_ssn.json")
    local_ssn = json.loads(fi.read())
    fi.close()
    j = 0
    ssn_list = local_ssn['RESULTS']
    random.shuffle(ssn_list)
    for i in ssn_list:
        print(f"Getting user info for: {i['SSN_NBR']}")
        r = client.get(url=f"http://localhost:8080/api/v1/user/{i['SSN_NBR']}")
        print(r.json())
        if j == user_count:
            break
        j+=1

def query_stations(count,client):
    for _ in range(count):
        print("getting stations")
        rr: httpx.Response = client.get(url="http://localhost:8080/api/v1/stations")
        print(rr.json())


def query_stations_ro(count, client):
    for _ in range(count):
        print("getting all stations ro")
        rr: httpx.Response = client.get(url="http://localhost:8080/api/v1/stations/ro")
        print(rr.json())

def query_stations_ro_assignable(count, client):
    for _ in range(count):
        print("getting all stations ro assignable")
        rr: httpx.Response = client.get(url="http://localhost:8080/api/v1/stations/roAssignable")
        print(rr.json())


def query_user_form(count, client):
    for _ in range(count):
        print("Getting user form data")
        r: httpx.Response = client.get(url="https://localhost:8080/api/v1/userForm")
        print(r.json())
        time.sleep(1)

# proxy="http://pgrady:UKtEknIiszL!41f*@localhost:8080:9443", verify="cacerts.pem"
def main():
    with (httpx.Client() as client,
          ThreadPoolExecutor(max_workers=5) as executor):
#        client.post()
        fs = list()
        for _ in range(0, 10):
            fs.append(executor.submit(query_stations_ro_assignable, 50, client))
            fs.append(executor.submit(query_users,200, client))
            fs.append(executor.submit(query_user_form,300, client))
            fs.append(executor.submit(query_stations_ro, 100, client))
            cf.wait(fs, return_when=ALL_COMPLETED) 
            

        
if __name__ == '__main__':
    main()
