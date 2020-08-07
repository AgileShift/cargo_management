# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

    # TODO: Make this validations!
    # def validate(self):
    #     if 'TBA' in self.tracking_number and self.carrier != 'AmazonMws':
    #         frappe.throw()

    def before_save(self):
        """ Before is saved But after validate. We add new data and save once. When Insert(Create) or Save(Update). """
        if self.can_track():  # Validate all checks if we can track the parcel.
            self._get_data_from_easypost_api()  # TODO: Validate if we have more tracking apis

    def get_carrier_flags(self):
        """ Return the carrier global flags settings handling the parcel as a dict. """
        return frappe.get_value('Parcel Carrier', self.carrier, fieldname=('can_track', 'uses_utc'), as_dict=True)

    def get_carrier_settings(self):
        """ Return a object with all the carrier global settings handling the parcel. """
        return frappe.get_doc('Parcel Carrier', self.carrier)

    def can_track(self):
        """ This def validate if a parcel can be tracked by any mean. """
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

    def _get_data_from_easypost_api(self):
        """ this def communicates with the API. """
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
                    self.status = 'waiting_confirmation'  # Pending a confirmation from the warehouse!

            elif carrier_details.status == 'in_transit':
                self.status = 'waiting_for_reception'

            frappe.publish_realtime('display_alert', message='Parcel has been updated.', user=frappe.session.user)
