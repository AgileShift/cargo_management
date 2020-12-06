import datetime

import easypost
import pytz

import frappe
from frappe import _


class EasypostAPIError(easypost.Error):
    """
    Child Class to personalize API Error
    https://www.easypost.com/errors-guide/python
    """
    pass


class EasypostAPI(object):
    """ Easypost methods to control class API and parse data. """

    def __init__(self, carrier_uses_utc):
        self.instance = {}
        self.carrier_uses_utc = carrier_uses_utc
        self.api_key = frappe.get_single('Parcel Settings').get_password('easypost_api_key')

    def create_package(self, tracking_number, carrier):
        """
        Create a Tracking Resource on Easypost API

        @param tracking_number: String Tracking Number
        @param carrier: String Code of Carrier
        """
        self.instance = easypost.Tracker.create(
            tracking_code=tracking_number,
            carrier=carrier,
            api_key=self.api_key
        )
        self._normalize_data()

    def retrieve_package_data(self, easypost_id):
        """ Retrieve from Easypost using the ID provided """
        self.instance = easypost.Tracker.retrieve(
            easypost_id=easypost_id,
            api_key=self.api_key
        )
        self._normalize_data()

    def convert_from_webhook(self, response):
        """ Convert a dict to a Easypost Object. """
        self.instance = easypost.convert_to_easypost_object(
            response=response,
            api_key=self.api_key
        )
        self._normalize_data()

    def _normalize_data(self):
        """ This normalize all the data will correct values """
        # Normalize Status
        self.instance.status = self.normalize_status(self.instance.status)
        self.instance.status_detail = self.normalize_status(self.instance.status_detail)

        # In easypost weight comes in ounces, we convert to pounds.
        self.instance.weight_in_pounds = self.instance.weight / 16 if self.instance.weight else 0.00

        # Normalize Dates. Some Carriers send the data in UTC others no
        self.instance.naive_est_delivery_date = self.naive_dt_to_local_dt(self.instance.est_delivery_date, self.carrier_uses_utc)

    @staticmethod
    def naive_dt_to_local_dt(dt_str, uses_utc):
        """
        Convert string datetime to unaware naive datetime;
        @param dt_str: EasyPost datetime format: 2020-06-015T06:00:00Z or 2020-06-015T06:00:00+00:00
        @param uses_utc: Boolean if time is UTC
        @return: datetime: Return naive it not using UTC else return local datetime, both are UTC unaware

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

    @staticmethod
    def normalize_status(status):
        """ Normalize to frappe conventions. Easypost send snake_case status, we use individual words titled """
        return status.replace('_', ' ').title()


@frappe.whitelist(allow_guest=True)
def easypost_webhook(**kwargs):
    """ POST To: {URL}/api/method/package_management.package_management.doctype.parcel.easypost_api.easypost_webhook """
    if kwargs['description'] != 'tracker.updated':
        return 'Post is not update.'  # This returns a 200 status.

    frappe.session.user = 'Easypost API'  # Quick Hack. Very useful

    try:
        parcel = frappe.get_doc('Parcel', kwargs['result']['tracking_code'])  # Trying to fetch the parcel Document
    except frappe.DoesNotExistError:
        return 'Parcel {} not found.'.format(kwargs['result']['tracking_code'])  # TODO: Add some log?
    else:
        parcel.load_carrier_flags()  # This is called on def can_track(). But we avoid that validation on webhook event.
        parcel.parse_data_from_easypost_webhook(kwargs)
        parcel.flags.ignore_validate = True  # Set flag ON because Doc will be saved from webhook data. No validations.
        parcel.save(ignore_permissions=True)  # Trigger before_save() who checks for the flag. We avoid all checks.

        # TODO: Translate: alert message and button
        parcel_route = "frappe.set_route('Form', 'Parcel', '{}')".format(parcel.tracking_number)
        alert_message = 'Parcel <a onclick="{0}">{1}</a> is {2}.'\
            .format(parcel_route, parcel.tracking_number, parcel.carrier_status)
        alert_body = '''
            <div class="next-action-container">
                <button onclick="{}" class="next-action"><span>{}</span></button>
            </div>
        '''.format(parcel_route, _('View'))

        frappe.publish_realtime(
            event='eval_js',  # https://discuss.erpnext.com/t/popup-message-using-frappe-publish-realtime/37286/7
            message='frappe.show_alert({}, 10);'.format({
                'body': alert_body,
                'message': alert_message,
                'indicator': 'blue'  # TODO: Indicator depends on carrier_status
            })
        )

    return 'Parcel {} updated.'.format(parcel.tracking_number)
