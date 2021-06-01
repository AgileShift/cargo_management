frappe.provide('frappe.dashboards.chart_sources');

frappe.dashboards.chart_sources["Packages by Type of Transport"] = {
	method: "cargo_management.package_management.dashboard_chart_source.packages_by_type_of_transport.packages_by_type_of_transport.get",
	filters: []
};