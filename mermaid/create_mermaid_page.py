import frappe

def execute():
    if not frappe.db.exists("Page", "mermaid"):
        page = frappe.get_doc({
            "doctype": "Page",
            "page_name": "mermaid",
            "title": "Mermaid Studio",
            "published": 1,
            "route": "mermaid",
            "template": "templates/pages/mermaid.html",
            "module": "Mermaid"
        })
        page.insert()
        frappe.db.commit()
        print("Mermaid page created")
    else:
        print("Mermaid page already exists")
