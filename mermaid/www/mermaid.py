import frappe
from frappe import _

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
        
        return context
    except Exception as e:
        frappe.log_error(f"Error in Mermaid Studio: {str(e)}")
        context.error = str(e)
        return context
