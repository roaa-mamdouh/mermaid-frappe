import unittest
import frappe
from frappe.utils import random_string

class TestMermaidDiagram(unittest.TestCase):
    def setUp(self):
        """Create test diagram before each test"""
        self.test_content = """
        graph TD
            A[Start] --> B[Process]
            B --> C{Decision}
            C -->|Yes| D[Result 1]
            C -->|No| E[Result 2]
            D --> F[End]
            E --> F
        """
        
        self.diagram = frappe.get_doc({
            "doctype": "Mermaid Diagram",
            "title": f"Test Diagram {random_string(8)}",
            "diagram_type": "Flowchart",
            "mermaid_content": self.test_content,
            "description": "Test diagram description"
        }).insert()

    def tearDown(self):
        """Clean up after each test"""
        frappe.delete_doc("Mermaid Diagram", self.diagram.name)

    def test_diagram_creation(self):
        """Test if diagram is created with correct values"""
        self.assertTrue(self.diagram.name)
        self.assertEqual(self.diagram.diagram_type, "Flowchart")
        self.assertEqual(self.diagram.mermaid_content.strip(), self.test_content.strip())
        
    def test_diagram_update(self):
        """Test updating diagram content"""
        new_content = """
        graph TD
            A[Start] --> B[End]
        """
        
        self.diagram.mermaid_content = new_content
        self.diagram.save()
        
        updated_doc = frappe.get_doc("Mermaid Diagram", self.diagram.name)
        self.assertEqual(updated_doc.mermaid_content.strip(), new_content.strip())
        
    def test_diagram_permissions(self):
        """Test diagram permissions"""
        # Create a test user
        test_user = "test@example.com"
        if not frappe.db.exists("User", test_user):
            frappe.get_doc({
                "doctype": "User",
                "email": test_user,
                "first_name": "Test",
                "send_welcome_email": 0
            }).insert()
        
        # Test private diagram
        self.diagram.is_public = 0
        self.diagram.save()
        
        # Switch to test user
        frappe.set_user(test_user)
        
        # Should not be able to read private diagram
        with self.assertRaises(frappe.PermissionError):
            frappe.get_doc("Mermaid Diagram", self.diagram.name)
        
        # Make diagram public
        frappe.set_user("Administrator")
        self.diagram.is_public = 1
        self.diagram.save()
        
        # Switch back to test user
        frappe.set_user(test_user)
        
        # Should be able to read public diagram
        doc = frappe.get_doc("Mermaid Diagram", self.diagram.name)
        self.assertTrue(doc)
        
        # Reset user
        frappe.set_user("Administrator")
        
    def test_diagram_search(self):
        """Test diagram search functionality"""
        from mermaid.mermaid.doctype.mermaid_diagram.mermaid_diagram import search_diagrams
        
        # Create a unique diagram for testing search
        unique_title = f"Unique Test Diagram {random_string(8)}"
        test_diagram = frappe.get_doc({
            "doctype": "Mermaid Diagram",
            "title": unique_title,
            "diagram_type": "Flowchart",
            "mermaid_content": self.test_content
        }).insert()
        
        # Search by title
        results = search_diagrams(unique_title)
        self.assertTrue(any(d.name == test_diagram.name for d in results))
        
        # Search by content
        results = search_diagrams("graph TD")
        self.assertTrue(len(results) > 0)
        
        # Cleanup
        frappe.delete_doc("Mermaid Diagram", test_diagram.name)
        
    def test_diagram_export(self):
        """Test diagram export functionality"""
        from mermaid.mermaid.doctype.mermaid_diagram.mermaid_diagram import export_diagram
        
        # Test SVG export
        svg_export = export_diagram(self.diagram.name, "svg")
        self.assertEqual(svg_export["mimetype"], "image/svg+xml")
        self.assertTrue(svg_export["filename"].endswith(".svg"))
        
        # Test Mermaid code export
        mmd_export = export_diagram(self.diagram.name, "mermaid")
        self.assertEqual(mmd_export["mimetype"], "text/plain")
        self.assertTrue(mmd_export["filename"].endswith(".mmd"))
        self.assertEqual(mmd_export["content"].strip(), self.diagram.mermaid_content.strip())
        
        # Test invalid format
        with self.assertRaises(frappe.ValidationError):
            export_diagram(self.diagram.name, "invalid")
            
    def test_diagram_duplicate(self):
        """Test diagram duplication"""
        from mermaid.mermaid.doctype.mermaid_diagram.mermaid_diagram import duplicate_diagram
        
        # Duplicate the diagram
        new_title = f"Duplicate Test {random_string(8)}"
        duplicate = duplicate_diagram(self.diagram.name, new_title)
        
        # Verify duplicate
        self.assertNotEqual(duplicate["name"], self.diagram.name)
        self.assertEqual(duplicate["title"], new_title)
        self.assertEqual(duplicate["content"], self.diagram.mermaid_content)
        
        # Cleanup
        frappe.delete_doc("Mermaid Diagram", duplicate["name"])
        
    def test_diagram_stats(self):
        """Test diagram statistics"""
        from mermaid.mermaid.doctype.mermaid_diagram.mermaid_diagram import get_diagram_stats
        
        stats = get_diagram_stats()
        
        # Verify stats structure
        self.assertIn("total", stats)
        self.assertIn("by_type", stats)
        self.assertIn("recent", stats)
        
        # Verify stats data
        self.assertIsInstance(stats["total"], int)
        self.assertGreater(stats["total"], 0)  # At least our test diagram
        self.assertTrue(any(d["diagram_type"] == "Flowchart" for d in stats["by_type"]))
