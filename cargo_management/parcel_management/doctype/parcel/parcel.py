import datetime

import frappe
from frappe import _
from frappe.model.document import Document
from cargo_management.parcel_management.doctype.parcel.api.easypost_api import EasyPostAPI, EasyPostAPIError
from cargo_management.parcel_management.doctype.parcel.api._17track_api import _17TrackAPI


class Parcel(Document):
	"""  All this are Frappe Core Flags:
		'ignore_links':       avoid: _validate_links()
		'ignore_validate':    avoid: validate() and before_save()
		'ignore_mandatory':   avoid: _validate_mandatory()
		'ignore_permissions': avoid: will not check for permissions globally.
	"""

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

		message, color = [], 'light-blue'  # TODO: Add more colors? Check frappe colors

		frappe.local.lang = 'es'  # Little Hack

		if self.status == 'Awaiting Receipt':
			message = ['El transporte aún no ha entregado el paquete.']

			if self.carrier_est_delivery:  # The carrier has provided an estimated delivery date
				est_delivery_diff = frappe.utils.date_diff(None, self.carrier_est_delivery)  # Diff from estimated to today
				est_delivery_date = frappe.utils.format_date(self.carrier_est_delivery, 'medium')  # readable date

				if est_delivery_diff == 0:  # Delivery is today
					message.append('La fecha programada de entrega es hoy.')
				elif est_delivery_diff == -1:  # Delivery is tomorrow
					message.append('La fecha programada es mañana.')
				elif est_delivery_diff < 0:  # Delivery is in the next days
					message.append('La fecha programada es: {}'.format(est_delivery_date))
				else:  # Delivery is late
					color = 'pink'
					message.append('Esta retrasado. Debio de ser entregado el: {}'.format(est_delivery_date))
					message.append('Contacte a su proveedor para obtener mas información.')
			else:
				color = 'yellow'
				message.append('No se ha indicado una fecha de entrega estimada.')
		elif self.status in ['Awaiting Confirmation', 'In Extraordinary Confirmation']:
			if self.carrier_real_delivery:
				message = [
					'El transporte indica que entregó: {}'.format(
						frappe.utils.format_datetime(self.carrier_real_delivery, "EEEE, d 'de' MMMM yyyy 'a las' h:mm a").capitalize()
					)
				]

				if self.signed_by:
					message.append('Firmado por: {}'.format(self.signed_by))

				# TODO: check against current user tz: Change None to now in local delivery place timezone
				delivered_since = frappe.utils.time_diff(None, self.carrier_real_delivery)  # datetime is UTC

				# TODO: Compare Against Workable days
				# Parcel has exceeded the 24 hours timespan to be confirmed. Same as: time_diff_in_hours() >= 24.00
				if delivered_since.days >= 1:  # The day starts counting after 1-minute difference
					color = 'red'
					delivered_since_str = 'Ha pasado 1 día' if delivered_since.days == 1 else 'Han pasado {} días'

					message.append(delivered_since_str.format(delivered_since.days))
				else:
					message.append('Por favor espera 24 horas hábiles para que el almacén confirme la recepción.')

			else:
				color = 'yellow'
				message = [
					'El transportista índico una fecha de entrega aproximada: {}'.format(
						frappe.utils.format_datetime(self.carrier_est_delivery, 'medium'))
				]

			if self.status == 'In Extraordinary Confirmation':
				color = 'pink'
				message.append('El paquete se encuentra siendo verificado de forma extraordinaria.')
		elif self.status == 'Awaiting Departure':
			# TODO: Add Warehouse Receipt date, # TODO: Add cargo shipment calendar
			cargo_shipment = frappe.get_cached_doc('Cargo Shipment', self.cargo_shipment)

			# TODO: What if we dont have real delivery date. Or signature
			message = [
				'El transportista indica que entrego el paquete el: {}.'.format(
					frappe.utils.format_datetime(self.carrier_real_delivery, 'medium')
				),
				'Firmado por {}'.format(self.carrier_real_delivery, self.signed_by),
				# 'Fecha esperada de recepcion en Managua: {}'.format(cargo_shipment.expected_arrival_date),

				# 'Embarque: {}'.format(self.cargo_shipment)
			]

		elif self.status == 'In Transit':
			# TODO: Add Departure date and est arrival date
			cargo_shipment = frappe.get_cached_doc('Cargo Shipment', self.cargo_shipment)

			color = 'purple'

			message = [
				'El paquete esta en transito a destino.',
				'Fecha de despacho: {}'.format(cargo_shipment.departure_date),
				'Fecha esperada de recepcion en Managua: {}'.format(cargo_shipment.expected_arrival_date),
				'Embarque: {}'.format(self.cargo_shipment)
			]

		elif self.status == 'In Customs':
			message, color = ['El paquete se encuentra en proceso de desaduanaje.'], 'gray'
		elif self.status in ['Sorting', 'To Bill']:
			message, color = ['El paquete se encuentra siendo clasificado en oficina.'], 'blue'
		elif self.status in ['Unpaid', 'For Delivery or Pickup']:
			message, color = ['El paquete esta listo para ser retirado.'], 'blue'
		elif self.status == 'Finished':
			message, color = ['Paquete Finalizado.'], 'green'  # TODO: Show invoice, delivery and payment details.
		elif self.status == 'Cancelled':
			message, color = ['Contáctese con un agente para obtener mayor información del paquete.'], 'orange'
		elif self.status == 'Never Arrived':
			message, color = ['El paquete no llego al almacén.'], 'red'
		elif self.status == 'Returned to Sender':
			message, color = ['El paquete fue devuelto por el transportista al vendedor.'], 'red'

		# Adding extra message
		if self.status in ['Never Arrived', 'Returned to Sender']:
			message.append('Contáctese con su vendedor y/o transportista para obtener mayor información.')

		return {'message': message, 'color': color}

	def request_data_from_api(self):
		""" This selects the corresponding API to request data. """
		carrier_api = frappe.get_file_json(frappe.get_app_path('Cargo Management', 'public', 'carriers.json'))['CARRIERS'][self.carrier].get('api')

		match carrier_api:
			case 'EasyPost':
				self._request_data_from_easypost_api()
				frappe.msgprint(_('Handling by EasyPost'), indicator='blue', alert=True)
			case '17Track':
				self._request_data_from_17track_api()
				frappe.msgprint(_('Handling by 17 Track'), indicator='blue', alert=True)
			case _:
				frappe.msgprint(_('Parcel is handled by a carrier we can\'t track.'), indicator='red', alert=True)

	def _request_data_from_easypost_api(self):
		""" Handles POST or GET to the Easypost API. Also parses the data. """
		try:
			if self.easypost_id:  # Parcel exists on easypost and is requested to be tracked. Request updates from API.
				api_data = EasyPostAPI(carrier=self.carrier).retrieve_package_data(self.easypost_id)
			else:  # Parcel don't exist on easypost and is requested to be tracked. We create a new one and attach it.
				api_data = EasyPostAPI(carrier=self.carrier).create_package(self.tracking_number)

				self.easypost_id = api_data.id  # EasyPost ID. Only on creation
		except EasyPostAPIError as e:
			frappe.msgprint(msg=str(e), title='EasyPost API Error', raise_exception=False, indicator='red')
			return  # Exit because this has failed(Create or Update)  # FIXME: don't throw because we need to save
		else:  # Data to parse that will be saved
			self._parse_data_from_easypost(api_data)

			frappe.msgprint(msg=_('Parcel has been updated from API.'), alert=True)

	def _request_data_from_17track_api(self):
		try:
			if self.is_new():
				api_data = _17TrackAPI().register_package(self.tracking_number, self.carrier)
			else:
				api_data = _17TrackAPI().retrieve_package_data(self.tracking_number)
		except Exception as e:
			if e.args[0]['code'] == -18019902:
				api_data = _17TrackAPI().register_package(self.tracking_number, self.carrier)
				self._request_data_from_17track_api()

			frappe.msgprint(msg=str(e), title='17Track API Error', raise_exception=False, indicator='red')
			return
		else:
			# parse and save data!
			print(self._parse_data_from_17track(api_data['track_info']))
			frappe.msgprint(msg=_('Parcel has been updated from API.'), alert=True)

	def parse_data_from_easypost_webhook(self, response):
		""" Convert an Easypost webhook POST to an Easypost Object, then parses the data to the Document. """
		easypost_api = EasyPostAPI(carrier=self.carrier)  # TODO
		easypost_api.convert_from_webhook(response['result'])  # This convert and normalizes the data

		self._parse_data_from_easypost(easypost_api.instance)

	def _parse_data_from_easypost(self, data):
		""" This parses all the data from an easypost Instance(with all the details) to our Parcel DocType. """

		self.carrier_status = data.status or 'Unknown'
		self.carrier_status_detail = data.status_detail or 'Unknown'

		self.signed_by = data.signed_by or None

		self.carrier_est_weight = data.weight_in_pounds
		self.carrier_est_delivery = data.naive_est_delivery_date

		# If parcel is delivered we get the last update details to lookup for the delivery datetime(real delivery date)
		if data.status == 'Delivered' or data.status_detail == 'Arrived At Destination':
			self.carrier_real_delivery = EasyPostAPI.naive_dt_to_local_dt(data.tracking_details[-1].datetime, EasyPostAPI.carriers_using_utc.get(self.carrier, False))  # FIXME: Improve this.
			self.change_status('Awaiting Confirmation')
		elif data.status == 'Return To Sender' or data.status_detail == 'Return':
			self.change_status('Returned to Sender')
		else:  # TODO: Change the status when the carrier status: failure, cancelled, error
			self.change_status('Awaiting Receipt')

		if data.tracking_details:
			last_detail = data.tracking_details[-1]

			self.carrier_last_detail = "<b>{status}</b> <br><br> {detail} <br><br> {location}".format(
				status=last_detail.message,
				detail=last_detail.description or 'Without Description',
				location="{city}, {state}, {zip}".format(
					city=last_detail.tracking_location.city or '',
					state=last_detail.tracking_location.state or '',
					zip=last_detail.tracking_location.zip or ''
				)
			)

	def _parse_data_from_17track(self, data):
		""" Parse data """
		print(data)

		self.carrier_status = data['latest_status']['status']
		self.carrier_status_detail = data['latest_status']['sub_status']

		# self.signed_by ?

		self.carrier_est_weight = float(data['misc_info']['weight_kg']) * 2.20  # FIXME: CHECK
		# self.carrier_est_delivery = data.time_metrics.estimated_delivery_date

		self.carrier_last_detail = data['latest_event']['description']

		if data['latest_status']['status'] == 'Delivered':
			self.carrier_real_delivery = datetime.datetime.strptime(data['latest_event']['time_iso'], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
			self.change_status('Awaiting Confirmation')
		else:
			self.carrier_status('Awaiting Receipt')
