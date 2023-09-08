import json
from datetime import datetime as dt

import easypost
#from easypost.errors import SignatureVerificationError

import frappe
from frappe.app import handle_exception


class EasyPostAPI:
	# The Dict Keys are the actual String representation for Users, and the Dict Values are the carrier code for the API
	# See more: https://www.easypost.com/docs/api#carrier-tracking-strings
	CARRIER_CODES: dict = {
		'DHL': 'DHLExpress',
		'SF Express': 'SFExpress',
	}

	# https://www.easypost.com/does-your-api-return-time-according-to-the-package-destinations-time-zone
	# https://support.easypost.com/hc/en-us/articles/360044353091#h_5ee616bd-5e42-4090-a6b3-44f8a54190cf
	CARRIER_USING_UTC: dict = {
		'FedEx': True
	}

	def __init__(self, carrier: str) -> None:
		self.data = {}
		self.carrier = self.CARRIER_CODES.get(carrier, carrier)
		# self.carrier_uses_utc = self.CARRIER_USING_UTC.get(carrier, False) # FIXME: This can be used with another carriers
		self.client = easypost.EasyPostClient(api_key=frappe.conf['easypost_api_key'])  # New EasyPost Client

	def register_package(self, tracking_number: str) -> dict:
		""" Register a Tracking on EasyPost API """
		easypost_obj = self.client.tracker.create(tracking_code=tracking_number, carrier=self.carrier)
		self.client.subscribe_to_request_hook(id=easypost_obj.id, url=frappe.conf['easypost_webhook_url'])
		return self._build_parcel_data(easypost_obj)

	def retrieve_package_data(self, easypost_id: str) -> dict:
		""" Retrieve data from EasyPost using the ID provided. """
		easypost_obj = self.client.tracker.retrieve(id=easypost_id)
		return self._build_parcel_data(easypost_obj)

	def convert_from_webhook(self, response) -> dict:
		""" Convert a dict to EasyPost Object. """
		easypost_obj = easypost.util.convert_to_easypost_object(response=response)
		return self._build_parcel_data(easypost_obj)

	def _build_parcel_data(self, easypost_obj) -> dict:
		""" Build our Object(Parcel Document) from EasyPost Object. """
		self.data: dict = {
			'easypost_id': easypost_obj.id,
			'signed_by': easypost_obj.signed_by,
			'carrier_status': frappe.unscrub(easypost_obj.status),                # Normalize Status
			'carrier_status_detail': frappe.unscrub(easypost_obj.status_detail),  # Normalize Status
			'carrier_est_weight': (easypost_obj.weight or 0.00) / 16.00,  # Weight comes in Ounces, we convert to Pounds
		}

		# Searching for the carrier_est_delivery. If it comes in local time or comes generalized
		if (detail := easypost_obj.carrier_detail) and (
			(date_local := detail.est_delivery_date_local) and (time_local := detail.est_delivery_time_local)
		):
			self.data['carrier_est_delivery'] = dt.fromisoformat(date_local + 'T' + time_local).replace(tzinfo=None)
		elif easypost_obj.est_delivery_date:
			self.data['carrier_est_delivery'] = dt.fromisoformat(easypost_obj.est_delivery_date).replace(tzinfo=None)

			if self.data['carrier_est_delivery'].time() == dt.min.time():  # If midnight, set to end of the day!
				self.data['carrier_est_delivery'] = self.data['carrier_est_delivery'].replace(hour=23, minute=59)

		if easypost_obj.tracking_details:  # Build the latest event detail. If 'Delivered', get the real delivery date
			latest = easypost_obj.tracking_details[-1]

			self.data['carrier_last_detail'] = (
				f"<b>{latest.message}</b><br><br>"
				f"{latest.description or 'Without Description'}<br><br>"
				f"{latest.tracking_location.city or ''} {latest.tracking_location.state or ''} {latest.tracking_location.zip or ''}"
			)

			# If parcel is Delivered we get the 'real_delivery_date' from the Latest Event Timestamp
			if self.data['carrier_status'] == 'Delivered':
				self.data['carrier_real_delivery'] = dt.fromisoformat(latest.datetime).replace(tzinfo=None)

		return self.data


@frappe.whitelist(allow_guest=True, methods='POST')
def easypost_webhook(**kwargs):
	""" POST To: {URL}/api/method/cargo_management.parcel_management.doctype.parcel.api.easypost_api.easypost_webhook """
	kwargs.pop('cmd')  # Remove extra data added by Frappe
	frappe.session.user = 'EasyPost API'  # Quick Hack. Very useful

	try:
		data = easypost.util.validate_webhook(
			event_body=json.dumps(kwargs, separators=(",", ":")).encode(),  # frappe.as_json() adds params and wont work
			headers=frappe.request.headers, webhook_secret=frappe.conf['easypost_webhook_secret']
		)

		if data['description'] != 'tracker.updated':
			return 'Not a Tracker Update Webhook Event'

		parcel = frappe.get_doc('Parcel', {'tracking_number': data['result']['tracking_code']})  # Search Parcel
	except (KeyError, easypost.errors.SignatureVerificationError, frappe.DoesNotExistError) as e:
		frappe.log_error(
			f"EasyPost Webhook: {type(e).__name__} -> {e}",
			reference_doctype='Parcel', reference_name=kwargs.get('result', {}).get('tracking_code', None)
		)

		return handle_exception(e)  # Handle as same as in frappe/app.py | handles -> http_status_code
	else:
		data = EasyPostAPI(carrier=parcel.carrier).convert_from_webhook(response=data['result'])  # This creates obj

		parcel.update_from_api_data(api_data=data)

		# Set because doc will be saved from webhook data. No validations needed.
		parcel.flags.ignore_validate = parcel.flags.ignore_mandatory = parcel.flags.ignore_links = True
		parcel.save(ignore_permissions=True)

		return f"Parcel {parcel.tracking_number} updated."
