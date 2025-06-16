import frappe
from frappe.model.document import Document
import json
import re

class MermaidDiagram(Document):
    def validate(self):
        """Validate mermaid syntax and set metadata"""
        if self.mermaid_content:
            # Basic syntax validation
            self.validate_mermaid_syntax()
            
            # Auto-detect diagram type if not set
            if not self.diagram_type:
                self.diagram_type = self.detect_diagram_type()
        
        # Set created_by and modified_by
        if not self.created_by:
            self.created_by = frappe.session.user
        self.modified_by = frappe.session.user
    
    def validate_mermaid_syntax(self):
        """Basic validation of mermaid syntax"""
        content = self.mermaid_content.strip()
        
        if not content:
            frappe.throw("Mermaid content cannot be empty")
        
        # List of valid mermaid diagram keywords
        valid_keywords = [
            'graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 
            'stateDiagram', 'erDiagram', 'journey', 'gantt', 'pie',
            'gitgraph', 'C4Context', 'mindmap', 'timeline', 'zenuml',
            'sankey'
        ]
        
        first_line = content.split('\n')[0].strip()
        
        # Check if starts with valid keyword
        has_valid_keyword = any(first_line.startswith(keyword) for keyword in valid_keywords)
        
        if not has_valid_keyword:
            frappe.msgprint(
                "Warning: Diagram doesn't start with a recognized Mermaid keyword. "
                "This might cause rendering issues.",
                alert=True
            )
    
    def detect_diagram_type(self):
        """Auto-detect diagram type from content"""
        content = self.mermaid_content.strip().lower()
        first_line = content.split('\n')[0].strip()
        
        type_mapping = {
            'graph': 'Flowchart',
            'flowchart': 'Flowchart',
            'sequencediagram': 'Sequence Diagram',
            'classdiagram': 'Class Diagram',
            'statediagram': 'State Diagram',
            'erdiagram': 'Entity Relationship Diagram',
            'journey': 'User Journey',
            'gantt': 'Gantt Chart',
            'pie': 'Pie Chart',
            'gitgraph': 'Gitgraph',
            'c4context': 'C4 Context',
            'mindmap': 'Mindmap',
            'timeline': 'Timeline',
            'zenuml': 'ZenUML',
            'sankey': 'Sankey'
        }
        
        for keyword, diagram_type in type_mapping.items():
            if first_line.startswith(keyword):
                return diagram_type
        
        return "Flowchart"  # Default
    
    def on_update(self):
        """Broadcast real-time updates"""
        broadcast_update(self, "update")
    
    def after_insert(self):
        """Broadcast creation"""
        broadcast_update(self, "insert")

@frappe.whitelist()
def get_mermaid_diagram(name):
    """Get diagram data for real-time editing"""
    doc = frappe.get_doc("Mermaid Diagram", name)
    return {
        "name": doc.name,
        "title": doc.title,
        "mermaid_content": doc.mermaid_content,
        "diagram_type": doc.diagram_type,
        "modified": doc.modified
    }

@frappe.whitelist()
def update_mermaid_content(name, content, rendered_svg=None):
    """Update diagram content with real-time sync"""
    doc = frappe.get_doc("Mermaid Diagram", name)
    doc.mermaid_content = content
    
    if rendered_svg:
        doc.rendered_svg = rendered_svg
    
    doc.save()
    
    # Broadcast to other sessions
    frappe.publish_realtime(
        event="mermaid_diagram_updated",
        message={
            "name": name,
            "content": content,
            "rendered_svg": rendered_svg,
            "modified": doc.modified
        },
        room=f"mermaid_diagram_{name}"
    )
    
    return {"status": "success", "modified": doc.modified}

def broadcast_update(doc, event_type):
    """Broadcast document updates to subscribed clients"""
    frappe.publish_realtime(
        event=f"mermaid_diagram_{event_type}",
        message={
            "name": doc.name,
            "title": doc.title,
            "content": doc.mermaid_content,
            "diagram_type": doc.diagram_type,
            "modified": doc.modified
        },
        room=f"mermaid_diagram_{doc.name}"
    )

@frappe.whitelist()
def render_mermaid_svg(content):
    """Server-side SVG rendering (placeholder - actual rendering happens client-side)"""
    # This is a placeholder for server-side rendering if needed
    # In practice, we'll do client-side rendering with mermaid.js
    return {"svg": f"<!-- Mermaid content: {len(content)} characters -->"}

@frappe.whitelist()
def create_new_diagram(title, diagram_type="Flowchart", content="", description=""):
    """Create a new Mermaid diagram"""
    doc = frappe.new_doc("Mermaid Diagram")
    doc.title = title
    doc.diagram_type = diagram_type
    doc.mermaid_content = content
    doc.description = description
    doc.insert()
    
    return {
        "name": doc.name,
        "title": doc.title,
        "content": doc.mermaid_content
    }

@frappe.whitelist()
def duplicate_diagram(name, new_title=None):
    """Duplicate an existing diagram"""
    original = frappe.get_doc("Mermaid Diagram", name)
    
    doc = frappe.new_doc("Mermaid Diagram")
    doc.title = new_title or f"{original.title} (Copy)"
    doc.diagram_type = original.diagram_type
    doc.mermaid_content = original.mermaid_content
    doc.description = original.description
    doc.is_public = False  # Reset public flag for copies
    doc.insert()
    
    return {
        "name": doc.name,
        "title": doc.title,
        "content": doc.mermaid_content
    }

@frappe.whitelist()
def get_diagram_list(filters=None, limit=20, start=0):
    """Get list of diagrams with pagination"""
    filters = filters or {}
    
    # Add user filter if not system manager
    if not frappe.has_permission("Mermaid Diagram", "read"):
        filters["created_by"] = frappe.session.user
    
    diagrams = frappe.get_list(
        "Mermaid Diagram",
        fields=["name", "title", "diagram_type", "modified", "created_by", "is_public"],
        filters=filters,
        order_by="modified desc",
        limit=limit,
        start=start
    )
    
    return diagrams

@frappe.whitelist()
def search_diagrams(query, limit=10):
    """Search diagrams by title or content"""
    conditions = []
    
    if query:
        conditions.append(f"(title LIKE '%{query}%' OR mermaid_content LIKE '%{query}%')")
    
    # Add user filter if not system manager
    if not frappe.has_permission("Mermaid Diagram", "read"):
        conditions.append(f"created_by = '{frappe.session.user}'")
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    diagrams = frappe.db.sql(f"""
        SELECT name, title, diagram_type, modified, created_by
        FROM `tabMermaid Diagram`
        WHERE {where_clause}
        ORDER BY modified DESC
        LIMIT {limit}
    """, as_dict=True)
    
    return diagrams

@frappe.whitelist()
def export_diagram(name, format="svg"):
    """Export diagram in various formats"""
    doc = frappe.get_doc("Mermaid Diagram", name)
    doc.check_permission("read")
    
    if format == "svg":
        return {
            "content": doc.rendered_svg,
            "filename": f"{doc.title}.svg",
            "mimetype": "image/svg+xml"
        }
    elif format == "mermaid":
        return {
            "content": doc.mermaid_content,
            "filename": f"{doc.title}.mmd",
            "mimetype": "text/plain"
        }
    else:
        frappe.throw("Unsupported export format")

@frappe.whitelist()
def get_diagram_stats():
    """Get statistics about diagrams"""
    stats = {}
    
    # Total diagrams
    stats["total"] = frappe.db.count("Mermaid Diagram")
    
    # Diagrams by type
    stats["by_type"] = frappe.db.sql("""
        SELECT diagram_type, COUNT(*) as count
        FROM `tabMermaid Diagram`
        GROUP BY diagram_type
        ORDER BY count DESC
    """, as_dict=True)
    
    # Recent activity
    stats["recent"] = frappe.db.sql("""
        SELECT DATE(modified) as date, COUNT(*) as count
        FROM `tabMermaid Diagram`
        WHERE modified >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        GROUP BY DATE(modified)
        ORDER BY date DESC
        LIMIT 30
    """, as_dict=True)
    
    return stats

@frappe.whitelist()
def share_diagram(name, users=None, roles=None, public=False):
    """Share diagram with specific users or roles"""
    doc = frappe.get_doc("Mermaid Diagram", name)
    doc.check_permission("share")
    
    if public:
        doc.is_public = True
        doc.save()
    
    # Add specific user permissions
    if users:
        for user in users:
            frappe.share.add("Mermaid Diagram", name, user, read=1, write=1)
    
    # Add role permissions
    if roles:
        for role in roles:
            # This would require custom implementation for role-based sharing
            pass
    
    return {"status": "success"}
