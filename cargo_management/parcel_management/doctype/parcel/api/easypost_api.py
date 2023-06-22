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
	CARRIER_CODES: dict = {
		'DHL': 'DHLExpress',
		'SF Express': 'SFExpress',
	}

	# They Plan to return normalized dates:
	# https://www.easypost.com/does-your-api-return-time-according-to-the-package-destinations-time-zone
	# https://www.easypost.com/why-are-there-time-zone-discrepancies-on-trackers
	CARRIER_USING_UTC: dict = {
		'FedEx': True
	}

	def __init__(self, carrier: str) -> None:
		self.data = {}
		self.carrier = self.CARRIER_CODES.get(carrier, carrier)
		self.carrier_uses_utc = self.CARRIER_USING_UTC.get(carrier, False)
		self.client = easypost.EasyPostClient(api_key=frappe.conf['easypost_api_key'])  # New EasyPost Client

	def create_package(self, tracking_number: str) -> dict:
		""" Create a Tracking on Easypost API """
		easypost_obj = self.client.tracker.create(tracking_code=tracking_number, carrier=self.carrier)
		return self._build_parcel_obj(easypost_obj)

	def retrieve_package_data(self, easypost_id: str) -> dict:
		""" Retrieve data from Easypost using the ID provided. """
		easypost_obj = self.client.tracker.retrieve(id=easypost_id)
		return self._build_parcel_obj(easypost_obj)

	def convert_from_webhook(self, response) -> dict:
		""" Convert a dict to Easypost Object. """
		easypost_obj = easypost.util.convert_to_easypost_object(response=response)
		return self._build_parcel_obj(easypost_obj)

	def _build_parcel_obj(self, easypost_obj) -> dict:
		""" Build our Object(Parcel Document) from Easypost Data. """
		self.data: dict = {
			'id': easypost_obj.id,
			'signed_by': easypost_obj.signed_by,
			'carrier_status': frappe.unscrub(easypost_obj.status),                # Normalize Status
			'carrier_status_detail': frappe.unscrub(easypost_obj.status_detail),  # Normalize Status
			'carrier_est_weight': (easypost_obj.weight or 0.00) / 16.00,  # Weight comes in ounces, we convert to pounds

			# Some Carriers give dates in UTC others no
			'carrier_est_delivery': self.naive_dt_to_local_dt(easypost_obj.est_delivery_date, self.carrier_uses_utc)
		}

		if easypost_obj.tracking_details:  # Build the latest event detail
			last_event = easypost_obj.tracking_details[-1]

			self.data['carrier_last_detail'] = "<b>{status}</b><br><br>{desc}<br><br>{location}".format(
				status=last_event.message, desc=last_event.description or 'Without Description',
				location="{city} {state} {zip}".format(
					city=last_event.tracking_location.city or '',
					state=last_event.tracking_location.state or '',
					zip=last_event.tracking_location.zip or ''
				)
			)

			# If parcel is Delivered we get the 'real_delivery_date' from the Latest Event datetime
			if self.data['carrier_status'] == 'Delivered' or self.data['carrier_status_detail'] == 'Arrived At Destination':
				self.data['carrier_real_delivery'] = self.naive_dt_to_local_dt(last_event.datetime, self.carrier_uses_utc)

		return self.data

	@staticmethod
	def naive_dt_to_local_dt(dt_str: str, uses_utc: bool):
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

		if not uses_utc:  # API already give us local datetime. So no need to convert from UTC to local
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
			return 'Not a Tracker Update Webhook Event'

		parcel = frappe.get_doc('Parcel', data['result']['status'])  # Search Parcel using 'name' only
	except (KeyError, easypost.errors.SignatureVerificationError, frappe.DoesNotExistError) as e:
		error_detail = '{} -> {}'.format(type(e).__name__, e)
		frappe.log_error(
			'EasyPost Webhook: {}'.format(error_detail),
			reference_doctype='Parcel', reference_name=kwargs.get('result', {}).get('tracking_code', None)
		)  # FIXME: What about other exceptions?: Will have to test it. Do we really need to handle them differently?
		return error_detail
	else:
		data = EasyPostAPI(carrier=parcel.carrier).convert_from_webhook(response=data['result'])

		parcel._parse_data_from_easypost(data)  # FIXME: avoid using a private method

		parcel.flags.ignore_validate = True  # Set because doc will be saved from webhook data. No validations needed.
		parcel.save(ignore_permissions=True)

		return 'Parcel {} updated.'.format(parcel.tracking_number)
# FIXME: 149(Production) -> 166(New Way) -> 150 Production Again -> 145 Best Production!
