import requests
from resources.urls import base_url

"""
class APIRequest:
    # Function to send a request to the /tests/{stationId} endpoint
"""

"""
def send_request(station_id, command, payload=None):
    url = f'{base_url}/tests/{station_id}'
    data = {'command': command}
    if payload is not None:
        data['payload'] = payload
    response = requests.post(url, json=data)
    return response
"""


def send_api_request(station_id, command, payload=None):
    global response
    url = f"{base_url}{station_id}"
    data = {
        "command": command,
        "payload": payload
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        #       print(f"status code: {response.status_code}")
        response = {'result': response.json(), 'status': response.status_code}
        return response
    except requests.exceptions.RequestException as e:
        #       print(f"status code: {response.status_code}")
        print(f"Request failed: {e}")
        response = {'result': None, 'status': response.status_code}
        return response
