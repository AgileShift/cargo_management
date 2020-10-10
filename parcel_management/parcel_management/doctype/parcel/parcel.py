import frappe
from frappe.model.document import Document

from .easypost_api import EasypostAPI, EasypostAPIError


class Parcel(Document):
    """
    Parcel Doctype: a Package ;)

    custom flags = {
        'ignore_track_validation': True|False, # If we will ignore all can_track validations. Internal hardcoded bypass
        'carrier_can_track': True|False, # Carrier can track in API. Comes from DB
        'carrier_uses_utc': True|False,  # Carrier uses UTC date times. Comes from DB
    }
    """
    def validate(self):
        """
        TODO: USPS label has another length that the provided by the shipper
        """

        # Only uppercase tracking numbers
        self.tracking_number = self.tracking_number.upper()

        tracking_number_strip = self.tracking_number[:3]

        # TODO: What if, what happens in frontend?
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

        print('Before save')

        if self.can_track():
            if self.is_new():  # This simulate before_insert() BUT after validate()
                self._get_data_from_easypost_api()
            elif self.has_value_changed('carrier'):  # Already exists and the carrier has changed.
                frappe.msgprint('Carrier has changed, so we request new data.', title='The carrier has changed')
                self.easypost_id = None
                self._get_data_from_easypost_api()

    def get_carrier_flags(self):
        """ Return the carrier global flags settings handling the parcel as a dict. """
        return frappe.get_value('Parcel Carrier', self.carrier, fieldname=('can_track', 'uses_utc'), as_dict=True)

    def get_carrier_settings(self):
        """ Return a object with all the carrier global settings handling the parcel. """
        return frappe.get_doc('Parcel Carrier', self.carrier)

    def can_track(self):
        print('Can Track')
        """ This def validate if a parcel can be tracked by any mean using API """
        # TODO: Validate if any tracker API is enabled.

        if self.flags.ignore_track_validation:  # Bypass validations flag
            return True  # if set to ignore validations then go: this flag is set hardcoded so we can "trust".

        if not self.track:  # Parcel is not configured to be tracked, no matter if easypost_id exists.
            frappe.publish_realtime('display_alert', message='Parcel is configured not to track.', user=frappe.session.user)
            return False

        self.flags = self.get_carrier_flags()  # Load carrier global flags settings on object

        if not self.flags.can_track:  # Carrier is configured to not track. So we don't bother.
            frappe.publish_realtime('display_alert', message='Parcel is handled by a carrier we dont\'t track.', user=frappe.session.user)
            return False

        return True

    def can_change_status(self, new_status):
        """ Validate the current status of the package and validates if a change is possible.

        @return Boolean, String
        """
        if self.status == new_status:
            return False, 'No puede cambiar el mismo estado.'

        if (new_status == 'Awaiting Dispatch') and self.status in ['Awaiting Receipt', 'Awaiting Confirmation']:
            return True, 'El paquete esta esperando recepcion o confirmacion y ahora esta esperando salida de Miami.'
        else:
            return False, 'No se puede cambiar el status: {0} a {1}'.format(self.status, new_status)

    def _get_data_from_easypost_api(self):
        """ this def communicates with the API. """
        print('GETTING DATA FROM EASYPOST')
        try:
            if self.easypost_id:  # Parcel exists on easypost and is requested to be tracked. Request updates from API.
                carrier_details = EasypostAPI.get_package_data(self.easypost_id)

            else:  # Parcel don't exists on easypost and is requested to be tracked. we create a new one and attach it.
                carrier_details = EasypostAPI.create_package(self.tracking_number, self.carrier)

                self.easypost_id = carrier_details.id  # EasyPost ID. Only on creation

        except EasypostAPIError as e:
            frappe.msgprint(msg=str(e), title='EasyPost API Error', raise_exception=0, indicator='red')
            return  # Exit because this has failed(Create or Update)

        else:  # Data to save

            self.signed_by = carrier_details.signed_by  # TODO: if finished?
            self.carrier_status = carrier_details.status
            self.carrier_status_detail = carrier_details.status_detail
            self.carrier_est_weight = EasypostAPI.convert_weight_to_lb(carrier_details.weight)
            self.carrier_est_delivery = EasypostAPI.naive_dt_to_local_dt(carrier_details.est_delivery_date, self.flags.uses_utc)

            # If parcel is delivered, we get the last update details & delivery datetime
            if carrier_details.status == 'delivered' or carrier_details.status_detail == 'arrived_at_destination':
                self.carrier_real_delivery = EasypostAPI.naive_dt_to_local_dt(carrier_details.tracking_details[-1].datetime, self.flags.uses_utc)

                if self.status == 'waiting_for_reception':  # Parcel is delivered and we're waiting for reception
                    self.status = 'Awaiting Confirmation'  # Pending a confirmation from the warehouse!

            elif carrier_details.status == 'in_transit':
                self.status = 'Awaiting Receipt'

            self.carrier_last_detail = "{}\n\n{}".format(
                carrier_details.tracking_details[-1].message,
                carrier_details.tracking_details[-1].description or 'Sin Descripcion'
            )

            frappe.publish_realtime('display_alert', message='Parcel has been updated.', user=frappe.session.user)
#128 TODO: Delete this.