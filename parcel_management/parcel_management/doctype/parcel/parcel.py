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
        # TODO: USPS label has another length that the provided by the shipper

        self.tracking_number = self.tracking_number.upper()  # Only uppercase tracking numbers
        tracking_number_strip = self.tracking_number[:3]

        # TODO: What if, what happens in frontend. Translate
        if '1Z' in tracking_number_strip and self.carrier != 'UPS':
            frappe.throw('Tracking de UPS')
        elif any(s in tracking_number_strip for s in ['LY', 'LB']) and self.carrier != 'USPS':
            frappe.throw('Posiblemente Tracking de USPS')
        elif 'TBA' in tracking_number_strip and self.carrier != 'AmazonMws':
            frappe.throw('Tracking de Amazon')
        elif 'JJD' in tracking_number_strip:
            frappe.throw('Convertir a tracking de DHL')

    def before_save(self):
        """ Before is saved on DB, after is validated. Add new data and save once. On Insert(Create) or Save(Update) """

        if self.flags.saves_from_webhook:
            return  # Ignores the rest, we're not fetching, we're parsing and saving from API. No user involved.

        if self.can_track():
            if self.flags.requested_to_track or self.is_new():  # This simulate before_insert() BUT after validate()
                self._request_data_from_easypost_api()
            elif self.has_value_changed('carrier'):  # Already exists and the carrier has changed.
                frappe.msgprint('Carrier has changed, so we request new data.', title='The carrier has changed')
                self.easypost_id = None  # For the moment EasyPost has no way to update the carrier of a package.
                self._request_data_from_easypost_api()

    def can_track(self):
        """ This def validate if a parcel can be tracked by any mean using API, also loads the carrier flags. """
        # TODO: Validate if any tracker API is enabled.

        if self.flags.requested_to_track:  # Bypass validations flag
            return True  # if set to true then go. This flag is set hardcoded so we can "trust".

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
        carrier_flags = frappe.get_value('Parcel Carrier', self.carrier, fieldname=('can_track', 'uses_utc'), as_dict=True)

        self.flags.carrier_can_track = carrier_flags.can_track
        self.flags.carrier_uses_utc = carrier_flags.uses_utc

    def change_status(self, new_status):
        """ Validate the current status of the package and validates if a change is possible.

        @return Boolean, String
        """
        if self.status == new_status:
            return False, 'No puede cambiar el mismo estado.'
        elif new_status == 'Awaiting Confirmation' and self.status == 'Awaiting Receipt':
            return True, 'El paquete estaba esperando reception y ahora esta esperando confirmacion'
        elif new_status == 'Awaiting Dispatch' and self.status in ['Awaiting Receipt', 'Awaiting Confirmation']:
            return True, 'El paquete estaba esperando recepcion o confirmacion y ahora esta esperando salida de Miami.'
        elif new_status == 'In Transit' and self.status in ['Awaiting Receipt', 'Awaiting Confirmation', 'Awaiting Dispatch']:
            return True, ''
        else:
            return False, 'No se puede cambiar el status: {0} a {1}'.format(self.status, new_status)

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
        self.carrier_status_detail = instance.status_detail

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
