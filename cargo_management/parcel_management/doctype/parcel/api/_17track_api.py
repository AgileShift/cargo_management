import requests

import frappe


class _17TrackAPI:
	""" 17Track methods to control class API and parse data. """
	api_base = "https://api.17track.net/track/v2/"

	# The Dict Keys are the actual String representation for Users, and the Dict Values are the carrier code for the API
	# See More at: https://res.17track.net/asset/carrier/info/apicarrier.all.json
	carrier_codes = {
		'Amazon': 100143,  # Swiship it works
		'FedEx': 100003,
		'LaserShip': 100052,
		'Cainiao': 190271,
		'Yanwen': 190012
	}

	def __init__(self):
		self.api_key = frappe.conf['17track_api_key']

	def _build_request(self, endpoint, payload):
		url = self.api_base + endpoint

		return requests.request('POST', url=url, json=payload, headers={
			"content-type": "application/json",
			"17token": self.api_key
		})

	def register_package(self, tracking_number, carrier):
		""" Create a Tracking on 17Track """
		response = self._build_request('register', payload=[{
			"number": tracking_number,
			"carrier": carrier,
			"auto_detection": True,  # So we avoid sending the carrier?
		}])

		return response.json()

	def retrieve_package_data(self, tracking_number):
		""" Retrieve data from 17Track """
		response = self._build_request('gettrackinfo', payload=[{
			"number": tracking_number
		}])

		response = response.json()  # IMPROVE THIS

		if response['data']['accepted']:
			return response['data']['accepted'][0]
		elif response['data']['rejected']:
			raise Exception(response['data']['rejected'][0]['error'])

		return response.json()
