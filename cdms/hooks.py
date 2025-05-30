# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "cdms"
app_title = "CDMS"
app_publisher = "PT. Solusi Manufaktur Teknologi"
app_description = "Customs Document Management System"
app_icon = "octicon octicon-repo"
app_color = "purple"
app_email = "support@smartconsultant.co"
app_license = "MIT"
app_include_css = "/assets/cdms/css/cdms.css"
app_include_js = "/assets/cdms/js/cdms.js"

fixtures = [
    {"dt":"Custom Field", "filters": [["dt", "in", ("BOM", "Warehouse", "Customer", "Item", "Company", "Supplier", "Address", "Purchase Receipt", "Purchase Receipt Item", "Stock Entry", "Stock Entry Detail","Sales Invoice Item")]]}, 
    "Client Script", "Property Setter"
]

website_context = {
	"favicon": 	"/assets/cdms/images/favicon.ico",
	"splash_image": "/assets/cdms/images/Logom.png"
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/cdms/css/cdms.css"
# app_include_js = "/assets/cdms/js/cdms.js"

# include js, css files in header of web template
# web_include_css = "/assets/cdms/css/cdms.css"
# web_include_js = "/assets/cdms/js/cdms.js"

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
# get_website_user_home_page = "cdms.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "cdms.install.before_install"
# after_install = "cdms.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "cdms.notifications.get_notification_config"

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
# 		"cdms.tasks.all"
# 	],
# 	"daily": [
# 		"cdms.tasks.daily"
# 	],
# 	"hourly": [
# 		"cdms.tasks.hourly"
# 	],
# 	"weekly": [
# 		"cdms.tasks.weekly"
# 	]
# 	"monthly": [
# 		"cdms.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "cdms.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "cdms.event.get_events"
# }

