import './controls/transportation_multicheck';
import './utils/parcel_quick_entry';
import './controls/overrides';

frappe.provide('cargo_management');

cargo_management = {
	TRANSPORTATIONS: {
		'Sea': {icon: 'ship', color: 'blue'},
		'Air': {icon: 'plane', color: 'red'}
	},

	// With this we can handle all our App Status Indicator Colors
	get_indicator: (status) => [__(doc.status), {
		// TODO: WORK IN PROGRESS
	}[status], 'status,=,' + status],

	find_carrier_by_tracking_number(tracking_number) {
		tracking_number = tracking_number.trim().toUpperCase(); // Sanitize field

		let response = {carrier: 'Unknown', search_term: tracking_number, tracking_number}; // Default values

		if (!tracking_number || tracking_number.length <= 6)
			return response; // If data is not returned, fields will be erased. Affected Views: List, Form and QuickEntry

		// FIXME: Add More Carriers: 'LY', 'LB', 'LW'
		// TODO: AQ are china Post, LW are USPS => Check if new need to added
		Object.entries(frappe.boot['carriers']).find(([carrier, {regex}]) => {
			if (!regex) return false;
			const match = tracking_number.match(regex);

			// TODO: Create a Multiselect Control for Carriers
			if (match) {
				console.log(match);
				Object.assign(response, {carrier, search_term: match[1] || match[2] || match[3] || tracking_number}); // If a captured group exists add it
				return true;
			}
		});

		return response; // If no match is found, default values will be returned.
	},

	icon_html: (icon) => ` <i class="fa fa-${icon}"></i>`, // Watch the first whitespace

	transportation_formatter(transportation) {
		const opts = this.TRANSPORTATIONS[transportation];

		return `<span class="indicator-pill ${opts.color} filterable no-indicator-dot ellipsis" data-filter="transportation,=,${transportation}">
            <span class="ellipsis">${__(transportation)}${this.icon_html(opts.icon)}</span>
        </span>`; // See more of this on list/list_view.js -> get_indicator_html();
	},
	transportation_indicator(transportation) {
		const opts = this.TRANSPORTATIONS[transportation];

		return `<span class="indicator-pill no-indicator-dot whitespace-nowrap ${opts.color}" style="margin-left: 10px">
			<span>${__(transportation)}${this.icon_html(opts.icon)}</span>
		</span>`; // See more of this on ui/page.js -> set_indicator() and clear_indicator()
	},

	open_carriers_dialog(doc) {
		// This function creates a dialog with all possible carriers where a parcel can be tracked
		let fields = [...this._carrier_section_for_dialog(__('Tracking Number'), doc.tracking_number, doc.carrier)];

		if (doc.name !== doc.tracking_number) {
			fields.unshift(...this._carrier_section_for_dialog(__('Name'), doc.name));
		}

		if (doc.content) {
			doc.content.forEach((content, i) => {
				if (content.tracking_number) {
					fields.push(...this._carrier_section_for_dialog(__('Consolidated #{0}', [i + 1]), content.tracking_number));
				}
			});
		}

		new frappe.ui.Dialog({animate: false, size: 'small', minimizable: true, title: __('Search'), fields: fields}).show();
	},

	_carrier_section_for_dialog(label, tracking_number, carrier = null) {
		carrier = carrier || this.find_carrier_by_tracking_number(tracking_number).carrier;

		const urls = frappe.boot['carriers'][carrier]['tracking_urls'];
		let fields = [{fieldtype: 'Section Break', label: `${label} (${carrier}): ${tracking_number}`}];

		urls.forEach((url, i) => {
			fields.push({
				fieldtype: 'Button', label: url.label, input_class: "btn-block btn-primary",  // FIXME: btn-default
				click: () => window.open(url.url + tracking_number)
			});

			if (i < urls.length - 1) {
				fields.push({fieldtype: 'Column Break'});
			}
		});

		return fields;
	}

};
// TODO 98: Working on Frappe Boot Info!
// TODO: 135(Bracket) WORKING on TransportationMultiSelect Single Control
// 127 -> 1 error, 5 warning, 2 warning, 8 typos - 29 October 2025
// 120 -> 22 January 2026 -> Refactor for v16 Carrier Info on Frappe Boot(Already deleted some dead code)
