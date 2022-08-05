from . import __version__ as app_version

app_name = "cargo_management"
app_title = "Cargo Management"
app_publisher = "Agile Shift"
app_description = "Track Packages across multiple carriers."
app_icon = "icon-paper-clip"
app_color = "red"
app_email = "contacto@gruporeal.org"
app_license = "MIT"
source_link = "https://github.com/AgileShift/cargo_management"
# app_logo_url = '/assets/cargo_management/images/app-logo.svg'

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = ["cargo_management.bundle.css"]
app_include_js = ["cargo_management.bundle.js"]

# include js, css files in header of web template
# web_include_css = "/assets/cargo_management/css/package_management.css"
# web_include_js = "/assets/cargo_management/js/package_management.js"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
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

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
		"on_submit": "cargo_management.sales_customization.utils.sales_invoice_on_submit"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"cargo_management.tasks.all"
# 	],
# 	"daily": [
# 		"cargo_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"cargo_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"cargo_management.tasks.weekly"
# 	]
# 	"monthly": [
# 		"cargo_management.tasks.monthly"
# 	]
# }

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
		{"doctype": "Package"},
		{"doctype": "Warehouse Receipt"},
		{"doctype": "Cargo Shipment"},
		{"doctype": "Cargo Shipment Receipt"},
	]
}
