frappe.provide('frappe.dashboards.chart_sources');

frappe.dashboards.chart_sources["Packages by Type of Transport"] = {
	method: "cargo_management.package_management.dashboard_chart_source.packages_by_type_of_transport.packages_by_type_of_transport.get",
	filters: []
};

// We can't call this right away, will not work. FIXME: This dont work if chart is Refresh or Reset
// We use it because we need time_series filters and a Custom Chart dont have that option in core.
setTimeout(() => {
	// First find if any and delete
	frappe.dashboard.chart_group.widgets_list[0].action_area.find('.timespan-filter, .time-interval-filter').remove()

	frappe.dashboard.chart_group.widgets_list[0].render_time_series_filters() // Render new time_series
}, 1000);
