import './controls/transportation_multicheck';
import './quick_entry/parcel';
import './utils/list_view';
import './utils/form_view';
import './utils/carriers';

const cargo_management = frappe.provide('cargo_management');

Object.assign(cargo_management, {
	TRANSPORTATIONS: {
		'Sea': {icon: 'ship', color: 'blue'},
		'Air': {icon: 'plane', color: 'red'}
	},

	icon_html: (icon) => ` <i class="fa fa-${icon}"></i>`, // Watch the first whitespace

});
// TODO: 135(Bracket) WORKING on TransportationMultiSelect Single Control
// 127 -> 1 error, 5 warning, 2 warning, 8 typos - 29 October 2025
// 120 -> 22 January 2026 -> Refactor for v16 Carrier Info on Frappe Boot(Already deleted some dead code)
