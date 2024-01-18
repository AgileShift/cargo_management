from easypost.errors.api import ApiError as EasyPostAPIError

import frappe
from frappe import _
from frappe.model.document import Document
from .api.api_17track import API17Track
from .api.easypost_api import EasyPostAPI
from .constants import Status, StatusMessage
from .utils import ParcelStateMachine


class Parcel(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from cargo_management.parcel_management.doctype.parcel_content.parcel_content import ParcelContent
		from frappe.types import DF

		assisted_purchase: DF.Check
		cargo_shipment: DF.Link | None
		carrier: DF.Literal["Drop Off", "Pick Up", "Unknown", "Amazon", "USPS", "UPS", "DHL", "FedEx", "OnTrac", "Cainiao", "SF Express", "Yanwen", "YunExpress", "SunYou", "Pitney Bowes", "Veho"]
		carrier_est_delivery: DF.Datetime | None
		carrier_est_weight: DF.Float
		carrier_last_detail: DF.SmallText | None
		carrier_real_delivery: DF.Datetime | None
		carrier_status: DF.Literal["Unknown", "Pre Transit", "In Transit", "Out For Delivery", "Available For Pickup", "Delivered", "Return To Sender", "Failure", "Cancelled", "Error"]
		carrier_status_detail: DF.Data | None
		content: DF.Table[ParcelContent]
		customer: DF.Link | None
		customer_name: DF.Data | None
		easypost_id: DF.Data | None
		est_delivery_1: DF.Date | None
		est_delivery_2: DF.Date | None
		explained_status: DF.Data | None
		has_taxes: DF.Check
		notes: DF.SmallText | None
		order_number: DF.Data | None
		residential_address: DF.Check
		shipper: DF.Autocomplete | None
		shipping_amount: DF.Currency
		signed_by: DF.Data | None
		status: DF.Literal["Awaiting Receipt", "Awaiting Confirmation", "In Extraordinary Confirmation", "Awaiting Departure", "In Transit", "In Customs", "Sorting", "To Bill", "Unpaid", "For Delivery or Pickup", "Finished", "Cancelled", "Never Arrived", "Returned to Sender"]
		total: DF.Currency
		tracking_number: DF.Data
		transportation: DF.Literal["Sea", "Air"]
	# end: auto-generated types
	"""  All these are Frappe Core Flags:
		'ignore_links':       avoid: _validate_links()
		'ignore_validate':    avoid: validate() and before_save()
		'ignore_mandatory':   avoid: _validate_mandatory()
		'ignore_permissions': avoid: will not check for permissions globally.
	"""

	# TODO: Add Override Decorator for python 3.12
	# TODO: Replace frappe.get_doc for DoctypeClass import. for Typing Completion

	#@override
	def save(self, request_data_from_api=False, *args, **kwargs):
		""" Override def to change validation behaviour. Useful when called from outside a form. """
		if request_data_from_api:  # If True we fetch data from API, ignore ALL checks and save it.
			self.flags.ignore_permissions = self.flags.ignore_validate = self.flags.ignore_mandatory = self.flags.ignore_links = True
			self.request_data_from_api()

		return super(Parcel, self).save(*args, **kwargs)

	def validate(self):
		""" Sanitize fields """
		self.tracking_number = self.tracking_number.strip().upper()  # Only uppercase with no spaces

	def before_save(self):
		""" Before saved in DB and after validated. Add new data. This runs on Insert(Create) or Save(Update)"""
		if self.is_new():
			self.request_data_from_api()
			# TODO: WORK ON THIS CHANGE!
		elif self.has_value_changed('carrier') or self.has_value_changed('tracking_number'):  # Exists and data has changed
			self.easypost_id = None  # Value has changed. We reset the ID. FIXME: Move this when we have new APIs.
			self.request_data_from_api()
			frappe.msgprint("Carrier or Tracking Number has changed, we have requested new data.", indicator='yellow', alert=True)

	def change_status(self, new_status):
		"""
		Validates the current status of the parcel and change it if it's possible.

		# Parcel was waiting for receipt, now is mark as delivered. waiting for confirmation.
		# Parcel was waiting for receipt or confirmation and now is waiting for the departure.
		# Parcel was not received and not confirmed, but has appear on the warehouse receipt.

		# TODO: Validate this when status is changed on Form-View or List-View
		"""
		psm = ParcelStateMachine(status=self.status)

		psm.transition(new_status)

		if self.status != new_status and \
			(self.status == 'Awaiting Receipt' and new_status in ['Awaiting Confirmation', 'Returned to Sender']) or \
			(self.status in ['Awaiting Receipt', 'Awaiting Confirmation', 'In Extraordinary Confirmation', 'Cancelled'] and new_status == 'Awaiting Departure') or \
			(self.status == 'Awaiting Departure' and new_status == 'In Transit') or \
			(self.status in ['Awaiting Receipt', 'Awaiting Confirmation', 'In Extraordinary Confirmation', 'Awaiting Departure', 'In Transit', 'Cancelled'] and new_status == 'Sorting') or \
			(self.status not in ['Unpaid', 'For Delivery or Pickup', 'Finished'] and new_status == 'To Bill') or \
			(self.status == 'To Bill' and new_status == 'Unpaid'):
			self.status = new_status
			return True

		return False

	@property
	def explained_status(self):
		""" This returns a detailed explanation of the current status of the Parcel and compatible colors. """
		# TODO: Python 3.10: Migrate to switch case or Improve performance?
		# frappe.local.lang = LocaleLanguage.SPANISH  # Little Hack

		message, color = [], 'blue'  # TODO: Add more colors? Check frappe colors

		match self.status:
			case Status.AWAITING_RECEIPT:
				message = [StatusMessage.TRANSPORTATION_NOT_DELIVERED_YET]

				if self.carrier_est_delivery:  # The carrier has provided an estimated delivery date
					est_delivery_diff = frappe.utils.date_diff(None, self.carrier_est_delivery)  # Diff from estimated to today
					est_delivery_date = frappe.utils.format_date(self.carrier_est_delivery, 'medium')  # readable date

					if est_delivery_diff == 0:  # Delivery is today
						message.append(StatusMessage.ESTIMATED_DELIVERY_DATE_TODAY)
					elif est_delivery_diff == -1:  # Delivery is tomorrow
						message.append(StatusMessage.ESTIMATED_DELIVERY_DATE_TOMORROW)
					elif est_delivery_diff < 0:  # Delivery is in the next days
						# message.append('La fecha programada es: {}'.format(est_delivery_date))
						message.append(StatusMessage.ESTIMATED_DELIVERY_DATE.value.replace('[DATE]', est_delivery_date))
					else:  # Delivery is late
						color = 'pink'
						# message.append('Esta retrasado. Debio de ser entregado el: {}'.format(est_delivery_date))
						message.append(StatusMessage.DELAYED_DELIVERY_DATE.value.replace('[DATE]', est_delivery_date))
						message.append(StatusMessage.CONTACT_YOUR_PROVIDER_FOR_INFO)
				else:
					color = 'yellow'
					message.append(StatusMessage.NOT_DELIVERY_DATE_ESTIMATED)

			case Status.AWAITING_CONFIRMATION:
				message, color = self._awaiting_confirmation_or_in_extraordinary_confirmation()
			case Status.IN_EXTRAORDINARY_CONFIRMATION:
				message, color = self._awaiting_confirmation_or_in_extraordinary_confirmation()
			case Status.AWAITING_DEPARTURE:
				# TODO: Add Warehouse Receipt date, # TODO: Add cargo shipment calendar
				#cargo_shipment = frappe.get_cached_doc('Cargo Shipment', self.cargo_shipment)

				# TODO: What if we dont have real delivery date. Or signature
				message = [
					StatusMessage.TRANSPORTER_DELIVERY_DATE.value.replace(
					'[DATE]',
					frappe.utils.format_datetime(self.carrier_real_delivery, 'medium')
				),
				StatusMessage.SIGNED_BY.value.replace('[SIGNER]', self.signed_by)
				# 'Firmado por {}'.format(self.carrier_real_delivery, self.signed_by),
				# 'Fecha esperada de recepcion en Managua: {}'.format(cargo_shipment.expected_arrival_date),

				# 'Embarque: {}'.format(self.cargo_shipment)
				]
			case Status.IN_TRANSIT:
				# TODO: Add Departure date and est arrival date
				if not self.cargo_shipment:
					return {'message': [StatusMessage.NO_CARGO_SHIPPING], color: 'red'}

				cargo_shipment = frappe.get_cached_doc('Cargo Shipment', self.cargo_shipment)

				color = 'purple'

				message = [
					StatusMessage.PACKAGE_IN_TRANSIT_TO_DESTINATION,
					StatusMessage.DEPARTURE_DATE.value.replace('[DATE]', cargo_shipment.departure_date),
					StatusMessage.ESTIMATED_RECEPTION_DATE.value.replace('[DATE]', cargo_shipment.expected_arrival_date),
					StatusMessage.CARGO_SHIPMENT.value.replace('[SHIPMENT]', self.cargo_shipment)
				]
			case Status.IN_CUSTOMS:
				message, color = [StatusMessage.PACKAGE_IN_CUSTOMS], 'gray'
			case Status.SORTING:
				message, color = [StatusMessage.PACKAGE_IN_OFFICE_SORTING], 'blue'
			case Status.TO_BILL:
				message, color = [StatusMessage.PACKAGE_IN_OFFICE_SORTING], 'blue'

			case Status.UNPAID:
				message, color = [StatusMessage.PACKAGE_READY], 'blue'
			case  Status.FOR_DELIVERY_OR_PICKUP:
				message, color = [StatusMessage.PACKAGE_READY], 'blue'

			case Status.FINISHED:
				message, color = [StatusMessage.PACKAGE_FINISHED], 'green'  # TODO: Show invoice, delivery and payment details.
			case Status.CANCELLED:
				message, color = [StatusMessage.CONTACT_AGENT_FOR_PACKAGE_INFO], 'orange'
			case Status.NEVER_ARRIVED:
				message, color = [StatusMessage.PACKAGE_NEVER_ARRIVED], 'red'
				message.append(StatusMessage.CONTACT_FOR_MORE_INFO)
			case Status.RETURNED_TO_SENDER:
				message, color = [StatusMessage.PACKAGE_RETURNED], 'red'
				message.append(StatusMessage.CONTACT_FOR_MORE_INFO)

			case _:
				...

		return {'message': message, 'color': color}

	def request_data_from_api(self):
		""" This selects the corresponding API to request data. Using Polymorphism. """
		carrier_api = frappe.get_file_json(frappe.get_app_path('Cargo Management', 'public', 'carriers.json'))['CARRIERS'].get(self.carrier, {}).get('api')

		print('TRY: MATCHING THE CARRIER_API')
		match carrier_api:
			case 'EasyPost':
				api_data = self._request_data_from_easypost_api()
			case '17Track':
				api_data = self._request_data_from_17track_api()
			case _:
				frappe.msgprint(_('Parcel is handled by a carrier we can\'t track.'), indicator='red', alert=True)
				return

		if not api_data:  # HOTFIX: We should always return something?
			return  # If we don't return, the try will fail, and api_data.get will raise a big error(None has not .get())

		try:
			print('ELSE: UPDATING FROM API DATA')
			self.update_from_api_data(api_data)  # Data from API that will be saved
			frappe.msgprint(_('Parcel has been updated from {} API.').format(carrier_api), indicator='green', alert=True)
		except Exception as e:
			frappe.log_error(f"17Track API: {type(e).__name__} -> {e}", reference_doctype='Parcel', reference_name=api_data.get('data', {}).get('number', None))

		print('OUTSIDE TRY: Saliendo del TRY')

	def _request_data_from_easypost_api(self) :
		""" Handles POST or GET to the Easypost API. Also parses the data. """
		try:
			if self.easypost_id:  # Parcel exists on Database. Request updates from API.
				return EasyPostAPI(self.carrier).retrieve_package_data(self.easypost_id)
			else:  # Parcel don't exist on System or EasyPost. We create a new one and attach it.
				return EasyPostAPI(self.carrier).register_package(self.tracking_number)
		except EasyPostAPIError as e:
			print('EXCEPT: Catching inside the requestor')
			frappe.msgprint(msg=str(e.__dict__), title='EasyPost API Error', raise_exception=False, indicator='red')

	# FIXME: 6 - 10 - 81
	def _request_data_from_17track_api(self):
		try:
			if self.easypost_id:
				return API17Track(self.carrier).retrieve_package_data(self.tracking_number)
			else:
				api_data = API17Track(self.carrier).register_package(self.tracking_number)
				self.easypost_id = api_data['tag']  # api_data.get('tag', frappe.generate_hash(length=10))
				return api_data
		except Exception as e:
			frappe.msgprint(msg=str(e), title='17Track API Error', raise_exception=False, indicator='red')
			return None  # HOTFIX for "if not api_data:"

	def update_from_api_data(self, api_data: dict) -> None:
		""" This updates the parcel with the data from the API. """
		print(api_data)
		self.__dict__.update(api_data)  # Updating all the DICT to the Parcel DocType

		if api_data['carrier_status'] == 'Delivered':  # or api_data['carrier_status_detail'] == 'Arrived At Destination':
			self.change_status('Awaiting Confirmation')
		elif api_data['carrier_status'] == 'Return To Sender' or self.carrier_status_detail == 'Return':
			self.change_status('Returned to Sender')
		else:  # TODO: Change the status when the carrier status: failure, cancelled, error
			self.change_status('Awaiting Receipt')

	def _awaiting_confirmation_or_in_extraordinary_confirmation(self):
		if self.carrier_real_delivery:
			color = 'blue'
			message = [StatusMessage.TRANSPORTATION_DELIVERED_DATE.value.replace('[DATE]', frappe.utils.format_datetime(self.carrier_real_delivery,"EEEE, d 'de' MMMM yyyy 'a las' h:mm a").capitalize())]

			if self.signed_by:
				message.append(StatusMessage.SIGNED_BY.value.replace('[SIGNER]', self.signed_by))

				# TODO: check against current user tz: Change None to now in local delivery place timezone
				delivered_since = frappe.utils.time_diff(None, self.carrier_real_delivery)  # datetime is UTC

				# TODO: Compare Against Workable days
				# Parcel has exceeded the 24 hours timespan to be confirmed. Same as: time_diff_in_hours() >= 24.00
				if delivered_since.days >= 1:  # The day starts counting after 1-minute difference
					color = 'red'
					delivered_since_str = StatusMessage.HAS_BEEN_1_DAY if delivered_since.days == 1 else StatusMessage.HAS_BEEN_X_DAYS

					message.append(delivered_since_str.value.replace('[DAYS]', str(delivered_since.days)))
				else:
					message.append(StatusMessage.WAIT_FOR_24_HOURS_CONFIRMATION)

		else:
			color = 'yellow'
			message = [StatusMessage.TRANSPORTER_INDICATE_ESTIMATE_DELIVERY_DATE.value.replace('[DATE]',frappe.utils.format_datetime(self.carrier_est_delivery, 'medium'))]

		if self.status == Status.IN_EXTRAORDINARY_CONFIRMATION:
			color = 'pink'
			message.append(StatusMessage.PACKAGE_IN_EXTRAORDINARY_REVISION)

		return message, color

# 294(HOTFIX) -> 250(WORKING) FIXME: Better way to update the doc: create some core method that returns a Object that we can concat :D
# 248 EasyPost DONE, Now 17 Track -> 238(Production | We need to avoid extra 'try')
# 241: Retornanos data normalizada desde las API, ahora debemos de hacer Polymorphism to select the API's

# FIXME: 19 warning, 20 w warning, 83 typos -> 287
# FIXME: 2 warning, 20 w warning, 85 typos -> 276
# 292 Refactor de constantes y estados
# FIXM:E 311: 2 warning, 29 w warning, 21 typos -> 276 | Corregir State Machine y COLOR usage!
