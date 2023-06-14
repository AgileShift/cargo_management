import datetime
import json

import easypost
import pytz

import frappe


class EasyPostAPIError(easypost.errors.EasyPostError):
	""" Child Class to personalize API Error """
	# https://www.easypost.com/errors-guide/python
	pass


class EasyPostAPI:
	""" Easypost methods to control class API and parse data. """

	# The Dict Keys are the actual String representation for Users, and the Dict Values are the carrier code for the API
	# See more: https://www.easypost.com/docs/api#carrier-tracking-strings
	carrier_codes = {
		'DHL': 'DHLExpress',
		'SF Express': 'SFExpress',
		'LaserShip': 'LaserShipV2'
	}

	# They Plan to return normalized dates:
	# https://www.easypost.com/does-your-api-return-time-according-to-the-package-destinations-time-zone
	# https://www.easypost.com/why-are-there-time-zone-discrepancies-on-trackers
	carriers_using_utc = {
		'FedEx': True
	}

	def __init__(self, carrier):
		self.data = {}
		self.carrier = self.carrier_codes.get(carrier, carrier)
		self.carrier_uses_utc = self.carriers_using_utc.get(carrier, False)
		self.client = easypost.EasyPostClient(api_key=frappe.conf['easypost_api_key'])  # New EasyPost Client

	def create_package(self, tracking_number):
		""" Create a Tracking on Easypost API """
		self.data = self.client.tracker.create(tracking_code=tracking_number, carrier=self.carrier)
		return self._normalize_data()

	def retrieve_package_data(self, easypost_id):
		""" Retrieve data from Easypost using the ID provided. """
		self.data = self.client.tracker.retrieve(id=easypost_id)
		return self._normalize_data()

	def convert_from_webhook(self, response):
		""" Convert a dict to Easypost Object. """
		self.data = easypost.util.convert_to_easypost_object(response=response)
		return self._normalize_data()

	def _normalize_data(self):
		""" This normalizes the data will correct values """
		self.data._unsaved_values = set()  # FIXME: EasyPost 8.0.0 is giving some sort of errors if this is not set.

		# Normalize Status
		self.data.status = frappe.unscrub(self.data.status)
		self.data.status_detail = frappe.unscrub(self.data.status_detail)

		# In easypost weight comes in ounces, we convert to pound.
		self.data.weight_in_pounds = self.data.weight / 16 if self.data.weight else 0.00

		# Normalize Dates. Some Carriers send the data in UTC others no. FIXME: EasyPost now gives us: est_delivery_date_local
		self.data.naive_est_delivery_date = self.naive_dt_to_local_dt(self.data.est_delivery_date, self.carrier_uses_utc)

		# Build the latest event detail
		if self.data.tracking_details:
			last_event = self.data.tracking_details[-1]

			self.data.latest_event = "<b>{status}</b><br><br>{desc}<br><br>{location}".format(
				status=last_event.message, desc=last_event.description or 'Without Description',
				location="{city} {state} {zip}".format(
					city=last_event.tracking_location.city or '',
					state=last_event.tracking_location.state or '',
					zip=last_event.tracking_location.zip or ''
				)
			)

		return self.data

	@staticmethod
	def naive_dt_to_local_dt(dt_str, uses_utc: bool):
		"""Convert string datetime to unaware naive datetime.

		@param dt_str: EasyPost datetime format: 2020-06-015T06:00:00Z or 2020-06-015T06:00:00+00:00
		@param uses_utc: Boolean if time is in UTC

		@return: datetime: Return naive if not using UTC else return local datetime, both are UTC unaware

		Some carriers already return datetime without UTC, its localized:
		https://www.easypost.com/does-your-api-return-time-according-to-the-package-destinations-time-zone
		https://www.easypost.com/why-are-there-time-zone-discrepancies-on-trackers
		"""

		if not dt_str:  # Sometimes datetime string if empty for some values, so return None value.
			return

		# Parse datetime from string; At this moment we don't know if it's in UTC or local.
		naive_datetime = datetime.datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S%z')

		if not uses_utc:  # API already give us local datetime. So no need to convert to local from UTC
			return naive_datetime.replace(tzinfo=None)

		# TODO: Make this conversion warehouse location aware!. For now we're pretending only Miami is local timezone
		local_tz = pytz.timezone('America/New_York')  # https://stackoverflow.com/a/32313111/3172310

		# Return unaware local datetime: Converts unaware UTC datetime to aware UTC and then delete the timezone info.
		return naive_datetime.astimezone(tz=local_tz).replace(tzinfo=None)


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
			return 'Not for update'

		parcel = frappe.get_doc('Parcel', data['result']['tracking_code'])
	except easypost.errors.SignatureVerificationError as e:
		frappe.log_error('EasyPost Webhook: {}'.format(e), reference_doctype='Parcel', reference_name=kwargs['result']['tracking_code'])
		return 'HMAC Error: {}'.format(e)
	except frappe.DoesNotExistError as e:
		frappe.log_error('EasyPost Webhook: {}'.format(e), reference_doctype='Parcel', reference_name=kwargs['result']['tracking_code'])
		return '{}'.format(e)
	else:
		data = EasyPostAPI(carrier=parcel.carrier).convert_from_webhook(response=data['result'])

		parcel._parse_data_from_easypost(data)  # FIXME: avoid using a private method

		parcel.flags.ignore_validate = True  # Set because doc will be saved from webhook data. No validations needed.
		parcel.save(ignore_permissions=True)

		return 'Parcel {} updated.'.format(parcel.tracking_number)
