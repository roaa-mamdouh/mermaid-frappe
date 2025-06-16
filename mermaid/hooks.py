from frappe import _

app_name = "mermaid"
app_title = "Mermaid"
app_publisher = "Roaa"
app_description = "Mermaid Diagram Editor"
app_email = "roaa@axentor.co"
app_license = "mit"



# Includes in <head>
# Only include mermaid-init.js if needed
app_include_css = ["mermaid.bundle.css"]
app_include_js = [
    "/assets/mermaid/js/mermaid-init.js"
]

# Include js, css files in header of web template
web_include_css = []
web_include_js = [
    "/assets/mermaid/js/mermaid-init.js"
]

# Website route rules
website_route_rules = [
    {"from_route": "/mermaid", "to_route": "mermaid"},
    {"from_route": "/mermaid-editor/<path:name>", "to_route": "mermaid-editor"},
]

# DocTypes
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": {"fieldname": ["in", ["mermaid_content", "mermaid_svg"]]}
    }
]

# Scheduled Tasks
scheduler_events = {
    # "all": [
    #     "mermaid.tasks.all"
    # ],
    # "daily": [
    #     "mermaid.tasks.daily"
    # ],
    # "hourly": [
    #     "mermaid.tasks.hourly"
    # ],
    # "weekly": [
    #     "mermaid.tasks.weekly"
    # ]
    # "monthly": [
    #     "mermaid.tasks.monthly"
    # ]
}

# Testing
before_tests = "mermaid.install.before_tests"

# Override standard doctype methods
override_doctype_methods = {
    "Mermaid Diagram": {
        "validate": "mermaid.mermaid.doctype.mermaid_diagram.mermaid_diagram.validate_mermaid_syntax"
    }
}

# Real-time events
doc_events = {
    "Mermaid Diagram": {
        "on_update": "mermaid.mermaid.doctype.mermaid_diagram.mermaid_diagram.broadcast_update"
    }
}
# Apps
# ------------------

required_apps = []

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
	{
		"name": "mermaid",
		"logo": "/assets/mermaid/logo.png",
		"title": "Mermaid",
		"route": "/mermaid",
	}
]


# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"mermaid.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

def get_assets():
    return {
        "mermaid": {
            "js": [
                # Remove mermaid.bundle.js from here since we're using Vite
                # The Vite-built assets are served from /assets/mermaid/frontend/dist/
            ],
            "css": [
                # Remove any CSS from here since we're using Vite
            ]
        }
    }

def get_website_user_home_page(user):
    return "mermaid"
