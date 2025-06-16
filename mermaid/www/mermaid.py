import frappe
from frappe import _
import json
import os

no_cache = 1

def get_context(context):
    try:
        context.no_cache = 1
        context.title = _("Mermaid Studio")
        
        # Add CSRF token for API requests
        context.csrf_token = frappe.sessions.get_csrf_token()
        
        # Ensure the page exists
        if not frappe.db.exists("Page", "mermaid"):
            frappe.get_doc({
                "doctype": "Page",
                "name": "mermaid",
                "title": "Mermaid Studio",
                "icon": "box",
                "module": "Mermaid",
                "is_standard": 1,
                "published": 1
            }).insert()
        
        # Load Vite manifest to get hashed asset filenames
        manifest_path = os.path.join(
            frappe.get_app_path("mermaid"),
            "mermaid",
            "public",
            "frontend",
            "dist",
            ".vite",
            "manifest.json"
        )
        if os.path.exists(manifest_path):
            with open(manifest_path, "r") as f:
                manifest = json.load(f)
            index_entry = manifest.get("index.html", {})
            context.js_file = "/assets/mermaid/frontend/dist/" + index_entry.get("file", "")
            context.css_file = None
            css_files = index_entry.get("css", [])
            if css_files:
                context.css_file = "/assets/mermaid/frontend/dist/" + css_files[0]
        else:
            context.js_file = "/assets/mermaid/frontend/dist/assets/index-CnysP75u.js"
            context.css_file = "/assets/mermaid/frontend/dist/assets/index-Degvk0vN.css"
        
        return context
    except Exception as e:
        frappe.log_error(f"Error in Mermaid Studio: {str(e)}")
        context.error = str(e)
        return context
