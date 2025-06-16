import frappe
from frappe import _

no_cache = 1

def get_context(context):
    """Get context for the Mermaid editor page"""
    
    # Get diagram name from route
    diagram_name = frappe.form_dict.get('name')
    
    if not diagram_name:
        # Create new diagram mode
        context.title = _("New Mermaid Diagram")
        context.diagram_data = {
            "name": None,
            "content": "",
            "title": ""
        }
        return context
    
    try:
        # Load existing diagram
        doc = frappe.get_doc("Mermaid Diagram", diagram_name)
        
        # Check permissions
        doc.check_permission("read")
        
        context.title = doc.title
        context.diagram_data = {
            "name": doc.name,
            "content": doc.mermaid_content,
            "title": doc.title
        }
        
    except frappe.DoesNotExistError:
        frappe.throw(_("Diagram not found"), frappe.NotFound)
    except frappe.PermissionError:
        frappe.throw(_("Not permitted to view this diagram"), frappe.PermissionError)
    
    return context
