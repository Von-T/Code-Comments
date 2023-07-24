from wso2 import get_token
import requests
import json

def dbconnect():
    lambda_endpoint = "https://api-qa.ucsd.edu:8243/sis-campus-information-collector/v1"
    token = get_token()
    return lambda_endpoint, token

"""
Sends a GET request to SIS API on WS02 to get data from HANA DB
"""
def select():
    try:
        lambda_endpoint, token = dbconnect()
        url = f"{lambda_endpoint}/metadata"

        headers = {
            "Authorization": f"Bearer {token}",
            "accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        return data

    except Exception as e:
        return str(e)

"""
Sends a GET request to SIS API on WS02 to get data on a specific entry with 'search_str' from HANA DB
"""
def selectname(search_str):
    try:
        lambda_endpoint, token = dbconnect()
        url = f"{lambda_endpoint}/metadata?search={search_str}"

        headers = {
            "Authorization": f"Bearer {token}",
            "accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        return data

    except Exception as e:
        return str(e)

"""
Sends a GET request to SIS API on WS02 to get data on a specific entry with 'id' from HANA DB
"""
def selectid(id):
    try:
        lambda_endpoint, token = dbconnect()
        url = f"{lambda_endpoint}/metadata?id={id}"

        headers = {
            "Authorization": f"Bearer {token}",
            "accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        return data

    except Exception as e:
        return str(e)

"""
Sends a POST request to SIS API on WS02 to post/update a list 'values' to some entry? 
(id is empty inside of 'values') to HANA DB
"""
def insert(values):
    try:
        lambda_endpoint, token = dbconnect()
        url = f"{lambda_endpoint}/metadata"

        headers = {
            "Authorization": f"Bearer {token}",
            "accept": "application/json"
        }

        payload = {
            "action": "insert",
            "values": values
        }

        response = requests.post(url, json=payload, headers=headers)
        result = response.json()

        return result

    except Exception as e:
        return str(e)

"""
Sends a POST request to SIS API on WS02 to post/update a list 'values' to an entry with
a certain 'id' (inside of 'values') to HANA DB
"""
def update(values):
    try:
        lambda_endpoint, token = dbconnect()
        url = f"{lambda_endpoint}/metadata"

        headers = {
            "Authorization": f"Bearer {token}",
            "accept": "application/json"
        }

        payload = {
            "action": "update",
            "values": values
        }

        response = requests.post(url, json=payload, headers=headers)
        result = response.json()

        return result

    except Exception as e:
        return str(e)