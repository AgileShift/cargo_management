import './controls/transportation_multicheck';
import './utils/parcel_quick_entry';
import './controls/overrides';

const cargo_management = frappe.provide('cargo_management');

Object.assign(cargo_management, {
	TRANSPORTATIONS: {
		'Sea': {icon: 'ship', color: 'blue'},
		'Air': {icon: 'plane', color: 'red'}
	},

	// TODO: Migrate to Document States? Maybe when frappe core starts using it.
	get_indicator: (status) => [__(status), {
		'Open': 'light-blue',

		'Awaiting Receipt': 'blue',
		'Awaiting Confirmation': 'orange',
		'In Extraordinary Confirmation': 'pink',
		'Awaiting Departure': 'yellow',
		'In Transit': 'purple',
		'In Customs': 'gray',
		'Sorting': 'green',
		'To Bill': 'green',
		'Unpaid': 'red',
		'For Delivery or Pickup': 'cyan',
		'Finished': 'darkgrey',
		'Cancelled': 'red',
		'Never Arrived': 'red',
		'Returned to Sender': 'red',
	}[status], 'status,=,' + status],

	find_carrier_by_tracking_number(tracking_number) {
		tracking_number = tracking_number.trim().toUpperCase(); // Sanitize field

		let response = {carrier: 'Unknown', search_term: tracking_number, tracking_number}; // Default values

		if (!tracking_number || tracking_number.length <= 6)
			return response; // If data is not returned, fields will be erased. Affected Views: List, Form and QuickEntry

		Object.entries(frappe.boot?.carriers || {}).some(([carrier, {regex}]) => {
			if (!regex) return false;
			const match = tracking_number.match(regex);

			if (!match) return false;

			// TODO: Create a Multiselect Control for Carriers
			Object.assign(response, {carrier, search_term: match[1] || match[2] || match[3] || tracking_number}); // If a captured group exist add it

			return true;
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

		let size = fields.length <= 6 ? 'small' : (fields.length <= 10 ? 'medium' : 'large'); // Dynamically set dialog size based on number of fields

		new frappe.ui.Dialog({animate: false, size: size, minimizable: false, title: __('Search'), fields: fields}).show();
	},

	_carrier_section_for_dialog(label, tracking_number, carrier = null) {
		carrier = carrier || this.find_carrier_by_tracking_number(tracking_number).carrier;

		const urls = frappe.boot['carriers'][carrier]['tracking_urls'];
		let fields = [{fieldtype: 'Section Break', label: `${label} (${carrier}): ${tracking_number}`}];

		urls.forEach((tracking_url, i) => {
			let input_class = tracking_url.type === 'Official' ?  'btn-primary' : tracking_url.type === 'Internal' ?  'btn-danger' :  'btn-info';
			fields.push({
				fieldtype: 'Button', label: tracking_url.label, input_class: `btn-block ${input_class}`,  // FIXME:  btn-primary
				click: () => window.open(tracking_url.url + tracking_number)
			});

			if (i < urls.length - 1) {
				fields.push({fieldtype: 'Column Break'});
			}
		});

		return fields;
	}

});
// TODO 98: Working on Frappe Boot Info!
// TODO: 135(Bracket) WORKING on TransportationMultiSelect Single Control
// 127 -> 1 error, 5 warning, 2 warning, 8 typos - 29 October 2025
// 120 -> 22 January 2026 -> Refactor for v16 Carrier Info on Frappe Boot(Already deleted some dead code)
