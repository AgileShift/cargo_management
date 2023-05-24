import {CARRIERS, DEFAULT_CARRIERS} from '../carriers.json' assert {type: 'json'};
import './utils/parcel_quick_entry';
import './controls/overrides';

frappe.provide('cargo_management');

cargo_management = {
	find_carrier_by_tracking_number(tracking_number) {
		tracking_number = tracking_number.trim().toUpperCase(); // Sanitize field

		let response = {carrier: 'Unknown', search_term: tracking_number, tracking_number};

		if (!tracking_number || tracking_number.length <= 6)
			return response; // If data is not returned, fields will be erased. Affected Views: List, Form and QuickEntry

		const carrierRegex = [ // The order matters for USPS and FedEx!
			{carrier: 'UPS',        regex: /^1Z/},
			{carrier: 'SunYou',     regex: /^SY/},       // SYUS & SYAE & SYBA
			{carrier: 'SF Express', regex: /^SF/},
			{carrier: 'Amazon',     regex: /^TBA/},
			{carrier: 'Cainiao',    regex: /^LP00/},     // Cainiao can sometimes track 'Yanwen' and 'SunYou'
			{carrier: 'DHL',        regex: /^.{10}$/},
			{carrier: 'YunExpress', regex: /^YT|^YU00/}, // These are sometimes delivered by USPS and LaserShip
			{carrier: 'LaserShip',  regex: /^1LS|^D100/},
			{carrier: 'Yanwen',     regex: /^ALS00|^S000|^UY/}, // ALS00 is sometimes delivered by USPS. UY ends with 'CZ'
			{carrier: 'Unknown',    regex: /^92(612.{17})$|^420.{5}92(612.{17})$/},       // *92612*90980949456651012 | 42033166*926129*0980949456651012. Start with: 92612 or with zipcode(420xxxxx) can be handled by FedEx or USPS. search_term starts at 612
			{carrier: 'USPS',       regex: /^9(?:.{21}|.{25})$|^420.{5}(9(?:.{21}|.{25}))$/}, // *9*400111108296364807659 | 42033165*9*274890983426386918697. First 8 digits: 420xxxxx(zipcode)
			{carrier: 'FedEx',      regex: /^.{12}$|^612.{17}$|^.{22}([1-9].{11})$/},     // *612*90982157320543198 | 9622001900005105596800*5*49425980480. Last 12 digits is tracking
		]; // FIXME: Sort by the most used Carrier? | FIXME: Add More Carriers: 'LY', 'LB', 'LW' | # FIXME: Move to carriers.json

		carrierRegex.find(({carrier, regex}) => {
			const match = tracking_number.match(regex);

			if (match) {
				Object.assign(response, {carrier, search_term: match[1] || match[2] || tracking_number}); // If a captured group exists add it
				return true;
			}
		});

		return response; // If no match is found, default values will be returned.
	},
	transportation_icon_html: (transportation) => ` <i class="fa fa-${transportation === 'Sea' ? 'ship' : 'plane'}"></i>`, // Watch the first whitespace
	transportation_formatter(transportation) {
		return `<span class="indicator-pill ${transportation === 'Sea' ? 'blue' : 'red'} filterable ellipsis"
            data-filter="transportation,=,${frappe.utils.escape_html(transportation)}">
            <span class="ellipsis">${transportation}${this.transportation_icon_html(transportation)}</span>
        <span>`; // Check get_indicator_html in list_view.js
	},
	load_carrier_settings(carrier_id) {
		// Returns Carrier Settings from carrier.json -> Used to build and config Action Buttons in Form
		const {api, tracking_url: main_url, default_carriers: extra_urls = []} = CARRIERS[carrier_id] || {};

		let urls = (main_url) ? [{'title': carrier_id, 'url': main_url}] : [];
		extra_urls.forEach(url_id => urls.push({'title': url_id, 'url': DEFAULT_CARRIERS[url_id]}));

		return {api, urls};
	}
};
