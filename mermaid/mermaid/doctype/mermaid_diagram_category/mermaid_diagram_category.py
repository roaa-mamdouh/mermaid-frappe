import frappe
from frappe.model.document import Document

class MermaidDiagramCategory(Document):
    def validate(self):
        """Validate category name"""
        if not self.category_name:
            frappe.throw("Category name cannot be empty")
        
        # Check for duplicate category names
        if frappe.db.exists("Mermaid Diagram Category", {
            "category_name": self.category_name,
            "name": ("!=", self.name)
        }):
            frappe.throw(f"Category '{self.category_name}' already exists")
