import frappe

def execute():
    page = frappe.get_doc("Page", "mermaid")
    print(page.as_dict())
