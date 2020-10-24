import frappe
from frappe.model.document import Document

from .easypost_api import EasypostAPI, EasypostAPIError


class Parcel(Document):
    """
    Parcel Doctype: a Package ;)

    custom flags = {
        'requested_to_track': True|False, # If we will ignore all can_track validations. Internal hardcoded bypass
        'saves_from_webhook': True|False, # If data comes from external API. We avoid all checks and just save.
        'carrier_can_track': True|False, # Carrier can track in API. Comes from DB
        'carrier_uses_utc': True|False,  # Carrier uses UTC date times. Comes from DB
    }
    """

    def validate(self):
        self.tracking_number = self.tracking_number.upper()  # Only uppercase tracking numbers
        tracking_number_strip = self.tracking_number[:3]

        # TODO: What if, what happens in frontend. Translate
        if '1Z' in tracking_number_strip and self.carrier != 'UPS':
            frappe.throw('Tracking de UPS')
        elif 'TBA' in tracking_number_strip and self.carrier != 'AmazonMws':
            frappe.throw('Tracking de Amazon')
        elif any(s in tracking_number_strip for s in ['LY', 'LB']) and self.carrier != 'USPS':
            frappe.throw('Posiblemente Tracking de USPS')
        elif 'JJD' in tracking_number_strip:
            frappe.throw('Convertir a tracking de DHL')

    def before_save(self):
        """ Before is saved on DB, after is validated. Add new data and save once. On Insert(Create) or Save(Update) """

        if self.flags.saves_from_webhook:
            return  # Ignores the rest, we're not fetching, we're parsing and saving from API. No user involved.

        if self.flags.requested_to_track:  # Bypass validations flag. This flag is set hardcoded so we can "trust".
            self._request_data_from_easypost_api()
            return

        if self.can_track():  # This is reach when the user has requested to save by normal conditions(Using Save btn).
            if self.is_new():  # Call this here because before_save() simulate before_insert() with a validate().
                self._request_data_from_easypost_api()
            elif self.has_value_changed('carrier'):  # Already exists and the carrier has changed.
                frappe.msgprint('Carrier has changed, so we request new data.', title='The carrier has changed')
                self.easypost_id = None  # For the moment EasyPost has no way to update the carrier of a package.
                self._request_data_from_easypost_api()

    def can_track(self):
        """ This def validate if a parcel can be tracked by any mean using API, also loads the carrier flags. """
        # TODO: Validate if any tracker API is enabled.

        if not self.track:  # Parcel is not configured to be tracked, no matter if easypost_id exists.
            frappe.publish_realtime('display_alert', message='Parcel is configured not to track.', user=frappe.session.user)
            return False

        self.load_carrier_flags()  # Load carrier global flags settings an attach to the document flags.

        if not self.flags.carrier_can_track:  # Carrier is configured to not track. So we don't bother.
            frappe.publish_realtime('display_alert', message='Parcel is handled by a carrier we dont\'t track.', user=frappe.session.user)
            return False

        return True

    def load_carrier_flags(self):
        """ Loads the carrier global flags settings handling the parcel in the flags of the Document. """
        self.flags.carrier_can_track, self.flags.carrier_uses_utc = \
            frappe.get_value('Parcel Carrier', filters=self.carrier, fieldname=['can_track', 'uses_utc'])

    def change_status(self, new_status):
        """ Validate the current status of the package and validates if a change is possible. """

        # Package was waiting for receipt, now is mark as delivered. waiting for confirmation.
        # Package was waiting for receipt or confirmation and now is waiting for the dispatch.
        # Package was not received, and not confirmed, but has appear on the warehouse receipt list

        if self.status != new_status and \
                (self.status == 'Awaiting Receipt' and new_status == 'Awaiting Confirmation') or \
                (self.status in ['Awaiting Receipt', 'Awaiting Confirmation'] and new_status == 'Awaiting Dispatch') or \
                (self.status == 'Awaiting Dispatch' and new_status == 'In Transit'):
            self.status = new_status
            print('From {0}, To {1}'.format(self.status, new_status))
            return True

        print('No Equivalente')
        print('Is {} was going to {}'.format(self.status, new_status))

    def get_explained_status(self):
        """ This returns a detailed explanation of the current status of the Parcel. """
        if self.status == 'Awaiting Receipt':
            message, color = 'Paquete aun no se entrega en almacen.', 'blue'
        elif self.status == 'Awaiting Confirmation':
            message, color = 'Paquete fue entregado segun el carrier, esperando confirmacion del almacen.', 'yellow'
        elif self.status == 'Awaiting Dispatch':
            message, color = 'Paquete fue recepcionado, esperando proximo despacho de mercaderia.', 'blue'
        elif self.status == 'In Transit':
            message, color = 'Paquete esta en transito a destino.', 'blue'
        else:
            message, color = 'Contactese para obtener mayor informacion del paquete.', 'yellow'

        return {'message': message, 'color': color}

    def parse_data_from_easypost_webhook(self, response):
        """ Convert the webhook POST to a Easypost Object, then parses the data to the Document. """
        easypost_api = EasypostAPI(carrier_uses_utc=self.flags.carrier_uses_utc)
        easypost_api.convert_from_webhook(response['result'])  # This convert and normalizes the data

        self._parse_data_from_easypost_instance(easypost_api.instance)

    def _request_data_from_easypost_api(self):
        """ Handles POST or GET to the Easypost API. Also parses the data. """
        try:
            easypost_api = EasypostAPI(carrier_uses_utc=self.flags.carrier_uses_utc)

            if self.easypost_id:  # Parcel exists on easypost and is requested to be tracked. Request updates from API.
                easypost_api.retrieve_package_data(self.easypost_id)
            else:  # Parcel don't exists on easypost and is requested to be tracked. we create a new one and attach it.
                easypost_api.create_package(self.tracking_number, self.carrier)

                self.easypost_id = easypost_api.instance.id  # EasyPost ID. Only on creation

        except EasypostAPIError as e:
            frappe.msgprint(msg=str(e), title='EasyPost API Error', raise_exception=0, indicator='red')
            return  # Exit because this has failed(Create or Update)

        else:  # Data to parse that will be save
            self._parse_data_from_easypost_instance(easypost_api.instance)

            frappe.publish_realtime('display_alert', message='Parcel has been updated.', user=frappe.session.user)

    def _parse_data_from_easypost_instance(self, instance):
        """ This parses all the data from an easypost instance(with all the details) to our Parcel Doctype """
        self.carrier_status = instance.status or 'Unknown'
        self.carrier_status_detail = instance.status_detail or 'Unknown'

        self.signed_by = instance.signed_by or None

        self.carrier_est_weight = instance.weight_in_pounds
        self.carrier_est_delivery = instance.naive_est_delivery_date

        # If parcel is delivered we get the last update details to lookup for the delivery datetime(real delivery date)
        if (instance.status == 'Delivered') or (instance.status_detail == 'Arrived At Destination'):
            self.carrier_real_delivery = EasypostAPI.naive_dt_to_local_dt(instance.tracking_details[-1].datetime, self.flags.carrier_uses_utc)
            self.change_status('Awaiting Confirmation')
        else:  # TODO: Change the status when the carrier status: return_to_sender, failure, cancelled, error
            self.change_status('Awaiting Receipt')

        if instance.tracking_details:
            latest_tracking_details = instance.tracking_details[-1]

            self.carrier_last_detail = "{}\n\n{}\n\n{}".format(
                latest_tracking_details.message,
                latest_tracking_details.description or 'Without Description',
                '{}, {}, {}'.format(  # TODO: Work this out!
                    latest_tracking_details.tracking_location.city,
                    latest_tracking_details.tracking_location.state or '',
                    latest_tracking_details.tracking_location.zip or ''
                )
            )


""" API Methods to communicate with the model that holds our business logic. """


@frappe.whitelist(allow_guest=False)
def get_parcel_explained_status(source_name):
    return frappe.get_doc('Parcel', source_name).get_explained_status()

#168