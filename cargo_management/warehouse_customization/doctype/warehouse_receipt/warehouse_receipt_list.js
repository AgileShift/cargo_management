frappe.listview_settings['Warehouse Receipt'] = {
    add_fields: ['status', 'transportation'],
    filters: [
        ['status', 'in', ['Draft', 'Open', 'Awaiting Departure']],
    ],
    hide_name_column: true,

    before_render() {
        localStorage.show_sidebar = "false"
    },

    get_indicator(doc) {
        const status_color = {
            'Draft': 'gray',
            'Open': 'orange',
            'Awaiting Departure': 'yellow',
            'In Transit': 'purple',
            'Sorting': 'orange',
            'Finished': 'green',
        };

        return [__(doc.status), status_color[doc.status], 'status,=,' + doc.status];
    },
    formatters: {
        transportation(val) {
            let color = (val === 'Sea') ? 'blue' : 'red';
            return `<span class="indicator-pill ${color} filterable ellipsis"
                data-filter="transportation,=,${frappe.utils.escape_html(val)}">
				<span class="ellipsis"> ${val} </span>
			<span>`;
        }
    }
}