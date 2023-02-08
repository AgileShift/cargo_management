import {CARRIERS, DEFAULT_CARRIERS} from '../carriers.json' assert {type: 'json'};
import './utils/parcel_quick_entry';
import './controls/overrides';

frappe.provide('cargo_management');

cargo_management = {
	find_carrier_by_tracking_number: function (tracking_number) {
        /* LINKED WITH: package_management/doctype/parcel/actions.py -> find_carrier_by_tracking_number

        Its specially made to avoid a call the server(API) to get a response that's does not have database data

        - https://pages.message.fedex.com/barcodescan_home/

        // TODO: Add More Carriers
        // FIXME: if only TBA, 1Z, 1LS is sent it should fail
        // FIXME: Run if tracking_number length is more than 6?
        */
        tracking_number = tracking_number.trim().toUpperCase();  // Sanitize field

        if (!tracking_number)
            return {};

        // TODO: search_term = 2/4 and 3/4 of the tracking. At bottom?
        let carrier = 'Unknown', search_term = tracking_number, tracking_number_len = tracking_number.length;

        if (tracking_number.slice(0, 3) === 'TBA') {
            carrier = 'Amazon';
        } else if (tracking_number.slice(0, 2) === '1Z') {
            carrier = 'UPS';
        } else if (tracking_number.slice(0, 3) === '1LS' || tracking_number.slice(0, 2) === 'D10') {
            carrier = 'LaserShip';
        } else if (tracking_number.slice(0, 4) === 'LP00') {
            carrier = 'Cainiao'; // Sometimes Cainiao can track 'Yanwen' and 'SunYou'
        } else if (tracking_number.slice(0, 2) === 'SF') {
            carrier = 'SF Express';
        } else if (tracking_number.slice(0 ,5) === 'ALS00' || tracking_number.slice(0, 3) === 'S00' || tracking_number.slice(0, 2) === 'UY') {
            carrier = 'Yanwen';
        } else if (tracking_number.slice(0, 2) === 'YT') {
            carrier = 'YunExpress';
        } else if (tracking_number.slice(0, 2) === 'SY') { //  SYUS && SYAE
            carrier = 'SunYou';
        }

        else if (tracking_number_len === 10) {
            carrier = 'DHL';
        } else if (tracking_number.slice(0, 2) === 'JD') {  // or JJD ?
            carrier = 'DHL';  // FIXME: Maybe we can convert it?
            frappe.show_alert({indicator: 'orange', message: __('Convert to DHL Tracking')});
        }

        // TODO: else if ( any(s in tracking_number for s in ['LY', 'LB', 'LW']) )
        //     return 'Possibly a USPS Tracking' || Can be tracked with Cainiao and USPS
        // TODO: YT: eg: YT2219421236038447

        // FedEx or USPS. Matches starting with: 92612 or with zipcode(420xxxxx). To search we will return starting with 612
        else if (tracking_number_len === 22 && tracking_number.slice(0, 5) === '92612') {
            carrier = ''; search_term = tracking_number.slice(2);        // *92612*90980949456651012. Or *926129*
        } else if (tracking_number_len === 30 && tracking_number.slice(8, 13) === '92612') {
            carrier = ''; search_term = tracking_number.slice(10);       // *42033166*92612*90980949456651012. Or *926129*
        }

        else if ([22, 26].includes(tracking_number_len) && tracking_number[0] === '9') {
            carrier = 'USPS';                                            // *9*400111108296364807659
        } else if ([30, 34].includes(tracking_number_len) && tracking_number[8] === '9') {
            carrier = 'USPS'; search_term = tracking_number.slice(8);    // 42033165*9*274890983426386918697. First 8 digits: 420xxxxx(zipcode)
        }

        else if (tracking_number_len === 12) {
            carrier = 'FedEx';
        } else if (tracking_number_len === 20 && tracking_number.slice(0, 3) === '612') {
            carrier = 'FedEx';                                           // *612*90982157320543198. Or *6129*
        } else if (tracking_number_len === 34 && tracking_number[22] !== '0') {
            carrier = 'FedEx'; search_term = tracking_number.slice(22);  // 9622001900005105596800*5*49425980480. Last 12 digits is tracking
        }

        return {
            'carrier': carrier,
            'search_term': search_term,
            'tracking_number': tracking_number
        };
    },
    transportation_icon_html: function (transportation) {
        return ` <i class="fa fa-${transportation === 'Sea' ? 'ship' : 'plane'}"></i>`; // Watch the first whitespace.
    },
    transportation_formatter: function (transportation) {
        return `<span class="indicator-pill ${transportation === 'Sea' ? 'blue' : 'red'} filterable ellipsis"
            data-filter="transportation,=,${frappe.utils.escape_html(transportation)}">
            <span class="ellipsis">${transportation}${this.transportation_icon_html(transportation)}</span>
        <span>`;
    },
    load_carrier_settings: function (carrier_id) {
        // Returns Carrier Settings from carrier.json -> Used to build and config Action Buttons in Form
        const {api, tracking_url: main_url, default_carriers: extra_urls = []} = CARRIERS[carrier_id] || {};

        let urls = (main_url) ? [{'title': carrier_id, 'url': main_url}] : [];
        extra_urls.forEach(url_id => urls.push({'title': url_id, 'url': DEFAULT_CARRIERS[url_id]}));

        return {api, urls};
    }
};
