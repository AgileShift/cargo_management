frappe.provide('frappe.dashboards.chart_sources');

frappe.dashboards.chart_sources["Packages by Type of Transport"] = {
    method: "cargo_management.parcel_management.dashboard_chart_source.packages_by_type_of_transport.packages_by_type_of_transport.get",
    filters: [
        {
            fieldname: "assisted_purchase",
            label: __("Assisted Purchase"),
            fieldtype: "Check"
        }
    ]
};

// We can't call this immediately, will not work. FIXME: This doesn't work if the chart is Refreshed or Reset
// We use this approach because we need time_series filters, and a Custom Chart doesn't have that option in the core.
setTimeout(() => {
    // First, find any existing instances and delete them
    frappe.dashboard.chart_group.widgets_list[0].action_area.find('.timespan-filter, .time-interval-filter').remove();

    frappe.dashboard.chart_group.widgets_list[0].render_time_series_filters(); // Render new time_series
}, 1000);
