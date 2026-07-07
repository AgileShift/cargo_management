const cargo_management = frappe.provide('cargo_management');

cargo_management.carriers = {
	find_by_tracking_number(tracking_number) {
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

	open_dialog(doc) {
		// This function creates a dialog with all possible carriers where a parcel can be tracked
		let fields = [...cargo_management.carriers._section_for_dialog(__('Tracking Number'), doc.tracking_number, doc.carrier)];

		if (doc.name !== doc.tracking_number) {
			fields.unshift(...cargo_management.carriers._section_for_dialog(__('Name'), doc.name));
		}

		if (doc.content) {
			doc.content.forEach((content, i) => {
				if (content.tracking_number) {
					fields.push(...cargo_management.carriers._section_for_dialog(__('Consolidated #{0}', [i + 1]), content.tracking_number));
				}
			});
		}

		let size = fields.length <= 6 ? 'small' : (fields.length <= 10 ? 'medium' : 'large'); // Dynamically set dialog size based on number of fields

		new frappe.ui.Dialog({animate: false, size: size, minimizable: false, title: __('Search'), fields: fields}).show();
	},

	_section_for_dialog(label, tracking_number, carrier = null) {
		carrier = carrier || cargo_management.carriers.find_by_tracking_number(tracking_number).carrier;

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
};
