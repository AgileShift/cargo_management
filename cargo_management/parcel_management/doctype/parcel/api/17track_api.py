import requests


class API17Track:
    """ 17Track methods to control class API and parse data. """
    api_key = None
    api_base = "https://api.17track.net/track/v2/"

    # The Dict Keys are the actual String representation for Users, and the Dict Values are the carrier code for the API
    carrier_codes = {
        'Amazon': 100143,  # Swiship it works
        'FedEx': 100003,
        'LaserShip': 100052,
        'Cainiao': 190271,
        'Yanwen': 190012
    }

    def build_request(self, endpoint, payload):
        url = self.api_base + endpoint

        return requests.request('POST', url=url, json=payload, headers={
            "content-type": "application/json",
            "17token": self.api_key
        })

    def create_package(self, tracking_number):
        """ Create a Tracking on 17Track """
        request = self.build_request('register', payload=[{
            "number": tracking_number,
            "auto_detection": True,
        }])

        print(request)

    def retrieve_package_data(self, tracking_number):
        """ Retrieve data from 17Track """
        request = self.build_request('gettrackinfo', payload=[{
            "number": tracking_number
        }])

        print(request)
