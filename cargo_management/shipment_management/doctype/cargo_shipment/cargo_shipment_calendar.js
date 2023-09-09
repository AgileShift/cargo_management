frappe.views.calendar['Cargo Shipment'] = {
    fields: ['departure_date', 'expected_arrival_date', 'name', 'reference', 'status'],
    field_map: {
        start: 'departure_date',
        end: 'expected_arrival_date', // TODO: What happens when the cargo shipment is received? end -> must be arrival_date
        id: 'name',
        title: 'name'
    },
    gantt: false,
    options: {
        header: {
 			left: 'prev,today,next',
 			center: 'title',
 			right: 'month,agendaWeek'
 		},
        eventStartEditable: false,  // Cannot edit even if editable is overridden in calendar.js
        selectable: false,
    },
    get_css_class: function(data) {
        if (data.status === 'Finished') return 'success';

        const days_from_today = frappe.datetime.get_diff(data.expected_arrival_date, frappe.datetime.get_today())
        if (days_from_today < 0) {
            return 'danger'; // Is late
        } else if (days_from_today === 0) {
            return 'warning'; // To arrive today!
        } else if (days_from_today > 0) {
            return 'default';
        }
    }
}
