import frappe
from frappe.model.document import Document

class MermaidDiagram(Document):
    def before_save(self):
        """Set metadata before saving"""
        if not self.creation_date:
            self.creation_date = frappe.utils.now()
            self.created_by = frappe.session.user
        
        self.modified_date = frappe.utils.now()
        self.modified_by = frappe.session.user

    def validate(self):
        """Validate the diagram code"""
        if not self.code:
            frappe.throw("Diagram code cannot be empty")
        
        if not self.title:
            self.title = "Untitled Diagram"
