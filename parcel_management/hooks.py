from . import __version__ as app_version

app_name = "parcel_management"
app_title = "Parcel Tracker Management"
app_publisher = "Agile Shift"
app_description = "Track parcels(Packages) across multiple carriers."
app_icon = "icon-paper-clip"
app_color = "red"
app_email = "contacto@agileshift.io"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/parcel_management/css/parcel_management.css"
# app_include_js = "/assets/parcel_management/js/parcel_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/parcel_management/css/parcel_management.css"
# web_include_js = "/assets/parcel_management/js/parcel_management.js"

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
# get_website_user_home_page = "parcel_management.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "parcel_management.install.before_install"
# after_install = "parcel_management.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "parcel_management.notifications.get_notification_config"

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

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"parcel_management.tasks.all"
# 	],
# 	"daily": [
# 		"parcel_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"parcel_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"parcel_management.tasks.weekly"
# 	]
# 	"monthly": [
# 		"parcel_management.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "parcel_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "parcel_management.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "parcel_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

