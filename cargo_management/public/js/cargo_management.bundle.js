import {CARRIERS, DEFAULT_CARRIERS} from '../carriers.json' assert {type: 'json'};
import './utils/parcel_quick_entry';
import './controls/overrides';

frappe.provide('cargo_management');

cargo_management = {
	find_carrier_by_tracking_number: function (tracking_number) {
        /* This JavaScript function replicates the corresponding Python function to prevent unnecessary API calls.
        By duplicating the functionality in JS, we can avoid making extra calls to the Python API.
        LINKED WITH: package_management/doctype/parcel/actions.py -> find_carrier_by_tracking_number */

        tracking_number = tracking_number.trim().toUpperCase();  // Sanitize field

		if (!tracking_number || tracking_number.length <= 4)
			return {};

		const carrierRegex = [ // USPS and FedEx the order matters!
			{carrier: 'UPS',        regex: /^1Z/},
			{carrier: 'SunYou',     regex: /^SY/},       // SYUS & SYAE & SYBA
			{carrier: 'SF Express', regex: /^SF/},
			{carrier: 'Amazon',     regex: /^TBA/},
			{carrier: 'Cainiao',    regex: /^LP00/},     // Sometimes Cainiao can track 'Yanwen' and 'SunYou'
			{carrier: 'DHL',        regex: /^.{10}$/},
			{carrier: 'YunExpress', regex: /^YT|^YU00/}, // Sometimes these are delivered by USPS and LaserShip
			{carrier: 'LaserShip',  regex: /^1LS|^D100/},
			{carrier: 'Yanwen',     regex: /^ALS00|^S000|^UY/}, // ALS00 sometimes delivered by USPS. UY ends with 'CZ'
			{carrier: 'Unknown',    regex: /^92(612.{17})$|^420.{5}92(612.{17})$/},       // *92612*90980949456651012 | 42033166*926129*0980949456651012. Start with: 92612 or with zipcode(420xxxxx) can be handled by FedEx or USPS. search_term starts at 612
			{carrier: 'USPS',       regex: /^9(?:.{21}|.{25})$|^420.{5}(9(?:.{21}|.{25}))$/}, // *9*400111108296364807659 | 42033165*9*274890983426386918697. First 8 digits: 420xxxxx(zipcode)
			{carrier: 'FedEx',      regex: /^.{12}$|^612.{17}$|^.{22}([1-9].{11})$/},    // *612*90982157320543198 | 9622001900005105596800*5*49425980480. Last 12 digits is tracking
		]; // FIXME: Sort by the most used Carrier | Add More Carriers: 'LY', 'LB', 'LW'.

		const result = carrierRegex.find(carrier => {
			const match = tracking_number.match(carrier.regex);

			if (match) {
				carrier.search_term = match[1] || match[2];  // We add the capture group if any and exit the loop.
				return true;
			}
		});

		return {
			'tracking_number': tracking_number,
            'carrier': result?.carrier ?? 'Unknown',
            'search_term': result?.search_term ?? tracking_number // If no captured group, then return whole string.
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
