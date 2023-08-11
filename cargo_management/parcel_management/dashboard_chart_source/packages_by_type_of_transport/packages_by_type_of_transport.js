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
