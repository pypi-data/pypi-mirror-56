name = "woyera"

import requests
import json

class WoyeraAPI:

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api-woyera.com/clean/"

    def clean(self, clean_type, data):
        full_url = self.url + clean_type + "/"
        request_body = {"apiKey": self.api_key, "data": data}

        r = requests.post(full_url, json=json.loads(json.dumps(request_body)))

        status_code = r.status_code
        json_response = r.json()

        if status_code == 200:
            results = json_response['cleanData']
        else:
            if 'error' in json_response:
                results = json_response['error']
            else:
                results = json_response

        return {"status_code": status_code, 'results': results}
