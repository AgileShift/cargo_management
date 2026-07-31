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
