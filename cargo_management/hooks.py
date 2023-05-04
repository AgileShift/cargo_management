from . import __version__ as app_version

app_name = "cargo_management"
app_title = "Cargo Management"
app_publisher = "Agile Shift"
app_description = "ERPNext Cargo Management for freight forwarders"
app_email = "contacto@gruporeal.org"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "cargo_management.bundle.css"
app_include_js = "cargo_management.bundle.js"

# include js, css files in header of web template
# web_include_css = "/assets/cargo_management/css/parcel_management.css"
# web_include_js = "/assets/cargo_management/js/parcel_management.js"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# Include js in doctype views: override/extend Standard Form Scripts.
doctype_js = {
	"Quotation": "public/js/quotation.js"  # TODO: WORKING HERE
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "cargo_management.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "cargo_management.install.before_install"
# after_install = "cargo_management.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "cargo_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events: Hook on document methods and events
doc_events = {
	"Sales Invoice": {  # TODO: WORKING
		"on_submit": "cargo_management.parcel_selling.utils.sales_invoice_on_submit"
	}
}

# Scheduled Tasks
scheduler_events = {
	# "all": [
	#	"cargo_management.parcel_management.doctype.parcel.events.check_parcel_delivery"
	# ],
}

# Testing
# -------

# before_tests = "cargo_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "cargo_management.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "cargo_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

global_search_doctypes = {
	"Default": [
		{"doctype": "Parcel"},
		{"doctype": "Warehouse Receipt"},
		{"doctype": "Cargo Shipment"},
		{"doctype": "Cargo Shipment Receipt"},
	]
}
