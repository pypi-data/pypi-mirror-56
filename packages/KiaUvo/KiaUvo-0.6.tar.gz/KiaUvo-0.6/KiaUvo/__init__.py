import requests
import json

from KiaUvo.models import AuthToken, Vehicle


class KiaUvo(object):
    default_headers = {
        'content-type': 'application/json;charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'host': 'www.myuvo.ca',
        'origin': 'https://www.myuvo.ca',
        'referer': 'https://www.myuvo.ca/login',
        'from': 'CWP',
        'language': '0',
        'offset': '0',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin'
    }

    base_url = 'https://www.myuvo.ca/tods/api/'

    def __init__(self, username, password, pin):
        self.vehicles = []
        self.engine_start_presets = []

        self.username = username
        self.password = password
        self.pin = pin

        self.auth = self.__login(username, password)
        self.verify_token()

    def login(self):
        self.auth = self.__login(self.username, self.password)
        self.verify_token()

    def __login(self, username, password):
        url = self.base_url + 'lgn'
        payload = {'loginId': username, 'password': password}
        headers = self.default_headers

        req = requests.post(url, data=json.dumps(payload), headers=headers)

        xhr = req.json()

        return AuthToken(xhr['result']['accessToken'], xhr['result']['refreshToken'])

    def verify_token(self):
        url = self.base_url + 'vrfytnc'
        headers = self.default_headers.copy()
        headers.update({
            'accessToken': self.auth.access_token
        })

        req = requests.post(url, headers=headers, data=json.dumps({}))

        return req.json()['result']

    def get_vehicle_list(self):
        url = self.base_url + 'vhcllst'
        headers = self.default_headers.copy()
        headers.update({
            'accessToken': self.auth.access_token
        })

        req = requests.post(url, headers=headers, data=json.dumps({}))

        return [self.get_vehicle_status(x['vehicleId']) for x in req.json()['result']['vehicles']]

    def get_vehicle_status(self, vehicle_id):
        print(vehicle_id)
        url = self.base_url + 'sltvhcl'
        headers = self.default_headers.copy()
        headers.update({
            'accessToken': self.auth.access_token,
            'vehicleId': vehicle_id
        })

        req = requests.post(url, headers=headers, data=json.dumps({}))
        result = req.json()['result']

        return Vehicle(result['vehicle'], result['status'], self.get_vehicle_maintenance(vehicle_id))

    def get_vehicle_maintenance(self, vehicle_id):
        url = self.base_url + 'nxtsvc'
        headers = self.default_headers.copy()
        headers.update({
            'accessToken': self.auth.access_token,
            'vehicleId': vehicle_id
        })

        req = requests.post(url, headers=headers, data=json.dumps({}))
        result = req.json()['result']

        return result["maintenanceInfo"]

    def update_vehicle_states(self):
        self.vehicles = self.get_vehicle_list()

    def request_vehicle_update(self, vehicle_id):
        # https://www.myuvo.ca/tods/api/rltmvhclsts
        print(vehicle_id)
        url = self.base_url + 'rltmvhclsts'
        headers = self.default_headers.copy()
        headers.update({
            'accessToken': self.auth.access_token,
            'vehicleId': vehicle_id
        })

        requests.post(url, headers=headers, data=json.dumps({}))

        self.vehicles = self.get_vehicle_list()

    def fetch_engine_start_presets(self, vehicle_id):
        # https://www.myuvo.ca/tods/api/gtfvsttng
        print(vehicle_id)
        url = self.base_url + 'gtfvsttng'
        headers = self.default_headers.copy()
        headers.update({
            'accessToken': self.auth.access_token,
            'vehicleId': vehicle_id
        })

        req = requests.post(url, headers=headers, data=json.dumps({}))
        result = req.json()['result']

        self.engine_start_presets = result

    def verify_pin(self, vehicle_id):
        # https://www.myuvo.ca/tods/api/vrfypin
        # {"pin":"0919"}

        print(vehicle_id)
        url = self.base_url + 'vrfypin'
        headers = self.default_headers.copy()
        headers.update({
            'accessToken': self.auth.access_token,
            'vehicleId': vehicle_id
        })

        req = requests.post(url, headers=headers, data=json.dumps({
            "pin": self.pin
        }))
        result = req.json()['result']

        return result['pAuth']

    def start_vehicle(self, vehicle_id, preset):
        pin_auth = self.verify_pin(vehicle_id)

        print(vehicle_id)
        url = self.base_url + 'rmtstrt'
        headers = self.default_headers.copy()
        headers.update({
            'accessToken': self.auth.access_token,
            'vehicleId': vehicle_id,
            'pAuth': pin_auth
        })

        req = requests.post(url, headers=headers, data=json.dumps({
            "pin": self.pin,
            "setting": preset
        }))

    def stop_vehicle(self, vehicle_id):
        pin_auth = self.verify_pin(vehicle_id)

        print(vehicle_id)
        url = self.base_url + 'rmtstp'
        headers = self.default_headers.copy()
        headers.update({
            'accessToken': self.auth.access_token,
            'vehicleId': vehicle_id,
            'pAuth': pin_auth
        })

        req = requests.post(url, headers=headers, data=json.dumps({
            "pin": self.pin
        }))

    def unlock_vehicle(self, vehicle_id):
        pin_auth = self.verify_pin(vehicle_id)

        print(vehicle_id)
        url = self.base_url + 'drulck'
        headers = self.default_headers.copy()
        headers.update({
            'accessToken': self.auth.access_token,
            'vehicleId': vehicle_id,
            'pAuth': pin_auth
        })

        req = requests.post(url, headers=headers, data=json.dumps({
            "pin": self.pin
        }))

    def lock_vehicle(self, vehicle_id):
        pin_auth = self.verify_pin(vehicle_id)

        print(vehicle_id)
        url = self.base_url + 'drlck'
        headers = self.default_headers.copy()
        headers.update({
            'accessToken': self.auth.access_token,
            'vehicleId': vehicle_id,
            'pAuth': pin_auth
        })

        req = requests.post(url, headers=headers, data=json.dumps({
            "pin": self.pin
        }))