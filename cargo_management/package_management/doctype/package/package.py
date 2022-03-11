import frappe
from frappe import _
from frappe.model.document import Document
from .easypost_api import EasypostAPI, EasypostAPIError


class Package(Document):
    """
    All these are set internally hardcoded. So we can trust in the origin.
    custom flags = {
        'ignore_validate':    Frappe Core Flag if is set avoid: validate() and before_save()
        'requested_to_track': If Package was requested to be tracked we bypass validate() and track on before_save().
        'carrier_can_track':  Carrier can track in API. Comes from related Link to "Package Carrier" Doctype.
        'carrier_uses_utc':   Carrier uses UTC date times. Comes from related Link to "Package Carrier" Doctype.
    }
    """

    def validate(self):
        """ Validate def. We try to detect a valid tracking number. """

        if self.flags.requested_to_track:  # If requested: bypass. We should have validated before set this flag.
            return

        # TODO: This is necessary?. Maybe only run at creation. This will work on API usage?
        self.tracking_number = self.tracking_number.strip().upper()  # Only uppercase tracking numbers

    def before_save(self):
        """ Before is saved on DB, after is validated. Add new data and save once. On Insert(Create) or Save(Update) """
        if self.flags.requested_to_track or (self.is_new() and self.can_track()):  # can_track can't run if is_new=False
            self._request_data_from_easypost_api()  # Track if is requested or is new and is able to track.
        elif not self.is_new() and self.has_value_changed('carrier') and self.can_track():  # Exists and carrier has changed
            frappe.msgprint(msg='Carrier has changed, we\'re requesting new data from the API.', title='Carrier Change')
            self.easypost_id = None
            self._request_data_from_easypost_api()
        # TODO: When track is recently set to active!

    def save(self, requested_to_track=None, ignore_validate=None, *args, **kwargs):
        """ Override to add custom flags. """
        self.flags.requested_to_track = requested_to_track
        self.flags.ignore_validate = ignore_validate

        return super(Package, self).save(*args, **kwargs)

    def load_carrier_flags(self):
        """ Loads the carrier global flags settings handling the package in the flags of the Document. """
        self.flags.carrier_can_track, self.flags.carrier_uses_utc = \
            frappe.get_cached_value('Package Carrier', self.carrier, fieldname=['can_track', 'uses_utc'])

    def can_track(self):
        """ This def validates if a package can be tracked by any mean using any API, also loads the carrier flags. """
        # TODO: Validate if a tracker API is enabled.
        return False
        if not self.track:  # Package is not configured to be tracked, no matter if easypost_id exists.
            frappe.msgprint(msg=_('Package is configured not to track.'), indicator='orange', alert=True)
            return False

        self.load_carrier_flags()  # Load carrier global flags settings and attach to the document flags.

        if not self.flags.carrier_can_track:  # Carrier is configured to not track. So we don't bother.
            frappe.msgprint(msg=_('Package is handled by a carrier we can\'t track.'), indicator='red', alert=True)
            return False

        return True

    def change_status(self, new_status):
        """
        Validates the current status of the package and change it if it's possible.

        # Package was waiting for receipt, now is mark as delivered. waiting for confirmation.
        # Package was waiting for receipt or confirmation and now is waiting for the departure.
        # Package was not received and not confirmed, but has appear on the warehouse receipt.

        # TODO: Validate this when status is changed on Form-View or List-View
        """

        if self.status != new_status and \
                (self.status == 'Awaiting Receipt' and new_status in ['Awaiting Confirmation', 'Returned to Sender']) or \
                (self.status in ['Awaiting Receipt', 'Awaiting Confirmation', 'In Extraordinary Confirmation', 'Cancelled'] and new_status == 'Awaiting Departure') or \
                (self.status == 'Awaiting Departure' and new_status == 'In Transit') or \
                (self.status in ['Awaiting Receipt', 'Awaiting Confirmation', 'In Extraordinary Confirmation', 'Awaiting Departure', 'In Transit', 'Cancelled'] and new_status == 'Sorting') or \
                (self.status not in ['Unpaid', 'To Deliver Or Pickup', 'Finished'] and new_status == 'To Bill') or \
                (self.status == 'To Bill' and new_status == 'Unpaid'):
            self.status = new_status
            return True

        return False

    def get_explained_status(self):
        """ This returns a detailed explanation of the current status of the Package and compatible colors. """
        # TODO: one of the best datetime format: "E d LLL yyyy 'at' h:MM a" # TODO: translate this strings.
        color = 'lightblue'  # TODO: Add more colors? Check frappe colors

        # TODO: If no Track or Easypost is not set(we can't track) show the alert. If is true and no est_delivery
        if self.status == 'Awaiting Receipt':
            message = ['El transportista aún no ha entregado el paquete.']

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
                    'El transportista indica que entrego el paquete el: {}.'.format(
                        frappe.utils.format_datetime(self.carrier_real_delivery, 'medium')
                    )
                ]

                delivered_since = frappe.utils.time_diff_in_seconds(None, self.carrier_real_delivery)  # datetime is UTC

                # Package has exceeded the 24 hours timespan to be confirmed. TODO: check against current user tz.
                if round(float(delivered_since) / 3600, 2) >= 24.00:  # Same as: time_diff_in_hours() >= 24.00
                    color = 'red'
                    message.append('Ha pasado: {} y el paquete aun no ha sido recibido por el almacén.'.format(
                        frappe.utils.format_duration(delivered_since)
                    ))
                else:
                    message.append('Por favor espera 24 horas hábiles para que el almacén confirme la recepción.')
            else:
                color = 'yellow'
                message = ['El transportista no índico una fecha de entrega.']

            if self.status == 'In Extraordinary Confirmation':
                color = 'pink'
                message.append('El paquete se encuentra siendo verificado de forma extraordinaria.')
        elif self.status == 'Awaiting Departure':
            # TODO: Add Warehouse Receipt date, # TODO: Add cargo shipment calendar
            message = ['El paquete fue recepcionado.', 'Esperando próximo despacho de carga.']
        elif self.status == 'In Transit':
            # TODO: Add Departure date and est arrival date
            message, color = 'El paquete esta en transito a destino.', 'purple'
        elif self.status == 'In Customs':
            message, color = 'El paquete se encuentra en proceso de desaduanaje.', 'gray'
        elif self.status == 'Sorting':
            message, color = 'El paquete se encuentra siendo clasificado en oficina.', 'blue'
        elif self.status == 'Available to Pickup':
            message, color = 'El paquete esta listo para ser retirado.', 'blue'
        elif self.status == 'Finished':
            return  # No message
        elif self.status == 'Never Arrived':
            message, color = ['El paquete no llego al almacén.'], 'red'
        elif self.status == 'Returned to Sender':
            message, color = ['El paquete fue devuelto por el transportista al vendedor.'], 'red'
        else:
            message, color = 'Contáctese con un agente para obtener mayor información del paquete.', 'orange'

        # Adding extra message
        if self.status in ['Never Arrived', 'Returned to Sender']:
            message.append('Contáctese con su vendedor y/o transportista para obtener mayor información.')

        return {'message': message, 'color': color}

    def parse_data_from_easypost_webhook(self, response):
        """ Convert an Easypost webhook POST to an Easypost Object, then parses the data to the Document. """
        easypost_api = EasypostAPI(carrier_uses_utc=self.flags.carrier_uses_utc)
        easypost_api.convert_from_webhook(response['result'])  # This convert and normalizes the data

        self._parse_data_from_easypost_instance(easypost_api.instance)

    def _request_data_from_easypost_api(self):
        """ Handles POST or GET to the Easypost API. Also parses the data. """
        try:
            easypost_api = EasypostAPI(carrier_uses_utc=self.flags.carrier_uses_utc)

            if self.easypost_id:  # Package exists on easypost and is requested to be tracked. Request updates from API.
                easypost_api.retrieve_package_data(self.easypost_id)
            else:  # Package don't exist on easypost and is requested to be tracked. We create a new one and attach it.
                easypost_api.create_package(self.tracking_number, self.carrier)

                self.easypost_id = easypost_api.instance.id  # EasyPost ID. Only on creation

        except EasypostAPIError as e:
            frappe.msgprint(msg=str(e), title='EasyPost API Error', raise_exception=False, indicator='red')
            return  # Exit because this has failed(Create or Update)  # FIXME: don't throw because we need to save

        else:  # Data to parse that will be saved
            self._parse_data_from_easypost_instance(easypost_api.instance)

            frappe.msgprint(msg=_('Package has been updated from API.'), alert=True)

    def _parse_data_from_easypost_instance(self, instance):
        """ This parses all the data from an easypost instance(with all the details) to our Package DocType. """
        self.carrier_status = instance.status or 'Unknown'
        self.carrier_status_detail = instance.status_detail or 'Unknown'

        self.signed_by = instance.signed_by or None

        self.carrier_est_weight = instance.weight_in_pounds
        self.carrier_est_delivery = instance.naive_est_delivery_date

        # If package is delivered we get the last update details to lookup for the delivery datetime(real delivery date)
        if instance.status == 'Delivered' or instance.status_detail == 'Arrived At Destination':
            self.carrier_real_delivery = EasypostAPI.naive_dt_to_local_dt(instance.tracking_details[-1].datetime, self.flags.carrier_uses_utc)
            self.change_status('Awaiting Confirmation')
        elif instance.status == 'Return To Sender' or instance.status_detail == 'Return':
            self.change_status('Returned to Sender')
        else:  # TODO: Change the status when the carrier status: failure, cancelled, error
            self.change_status('Awaiting Receipt')

        if instance.tracking_details:
            last_detail = instance.tracking_details[-1]

            self.carrier_last_detail = "<b>{status}</b> <br><br> {detail} <br><br> {location}".format(
                status=last_detail.message,
                detail=last_detail.description or 'Without Description',
                location="{city}, {state}, {zip}".format(
                    city=last_detail.tracking_location.city or '',
                    state=last_detail.tracking_location.state or '',
                    zip=last_detail.tracking_location.zip or ''
                )
            )
