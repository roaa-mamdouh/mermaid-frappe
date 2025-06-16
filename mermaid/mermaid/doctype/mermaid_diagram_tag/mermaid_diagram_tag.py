import frappe
from frappe.model.document import Document

class MermaidDiagramTag(Document):
    def validate(self):
        """Validate tag name"""
        if not self.tag:
            frappe.throw("Tag name cannot be empty")
