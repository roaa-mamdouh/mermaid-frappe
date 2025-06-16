from frappe import _

def get_data():
    return [
        {
            "module_name": "Mermaid",
            "color": "blue",
            "icon": "octicon octicon-project",
            "type": "module",
            "label": _("Mermaid Diagrams"),
            "description": _("Create and manage Mermaid diagrams"),
            "category": "Tools",
            "onboard_present": True,
            "onboard_data": {
                "youtube_id": None,  # Add tutorial video ID if available
                "help_links": [
                    {
                        "label": _("Create your first diagram"),
                        "url": "/app/mermaid-diagram/new"
                    },
                    {
                        "label": _("View documentation"),
                        "url": "https://github.com/your-repo/mermaid/wiki"
                    }
                ]
            }
        },
        {
            "module_name": "Mermaid Diagram",
            "color": "blue",
            "_doctype": "Mermaid Diagram",
            "icon": "octicon octicon-project",
            "type": "link",
            "link": "List/Mermaid Diagram",
            "label": _("Mermaid Diagrams"),
            "description": _("Create and manage Mermaid diagrams"),
            "onboard_present": True,
            "dependencies": ["Mermaid"],
            "quick_lists": [
                {
                    "label": _("My Recent Diagrams"),
                    "route": "List/Mermaid Diagram",
                    "filter": {
                        "owner": ["=", "user"]
                    }
                },
                {
                    "label": _("Public Diagrams"),
                    "route": "List/Mermaid Diagram",
                    "filter": {
                        "is_public": ["=", 1]
                    }
                }
            ]
        }
    ]

def get_module_sidebar_items():
    """Get module sidebar items for Mermaid module"""
    return {
        "Mermaid": [
            {
                "type": "doctype",
                "name": "Mermaid Diagram",
                "label": _("All Diagrams"),
                "description": _("View all diagrams"),
                "onboard": 1,
            },
            {
                "type": "doctype",
                "name": "Mermaid Diagram",
                "route_options": {
                    "is_public": 1
                },
                "label": _("Public Diagrams"),
                "description": _("View public diagrams"),
            },
            {
                "type": "doctype",
                "name": "Mermaid Diagram",
                "route": "/app/mermaid-diagram/new",
                "label": _("New Diagram"),
                "description": _("Create a new diagram"),
                "onboard": 1,
            },
            {
                "type": "page",
                "name": "mermaid-editor",
                "label": _("Diagram Editor"),
                "description": _("Open the diagram editor"),
                "onboard": 1,
            }
        ]
    }

def get_onboard_steps():
    """Get onboarding steps for Mermaid module"""
    return [
        {
            "title": _("Create Your First Diagram"),
            "description": _("Start by creating a new Mermaid diagram"),
            "route": "/app/mermaid-diagram/new",
            "action": _("New Diagram"),
            "is_complete": False,
            "is_skippable": False
        },
        {
            "title": _("Learn Mermaid Syntax"),
            "description": _("Learn how to create different types of diagrams"),
            "route": "https://mermaid.js.org/intro/",
            "action": _("View Guide"),
            "is_complete": False,
            "is_skippable": True
        },
        {
            "title": _("Share Your Diagram"),
            "description": _("Make your diagram public to share with others"),
            "route": "/app/mermaid-diagram",
            "action": _("View Diagrams"),
            "is_complete": False,
            "is_skippable": True
        }
    ]
