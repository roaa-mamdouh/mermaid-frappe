frappe.ui.form.on('Mermaid Diagram', {
    refresh: function(frm) {
        // Add custom buttons
        frm.add_custom_button(__('Open Editor'), function() {
            frappe.set_route('mermaid-editor', frm.doc.name);
        }, __('Actions'));
        
        frm.add_custom_button(__('Preview'), function() {
            show_mermaid_preview(frm);
        }, __('Actions'));
        
        // Setup real-time collaboration
        setup_realtime_sync(frm);
        
        // Initialize mermaid if content exists
        if (frm.doc.mermaid_content) {
            render_mermaid_preview(frm);
        }
    },
    
    mermaid_content: function(frm) {
        // Auto-save and re-render on content change
        if (frm.doc.mermaid_content) {
            debounced_render(frm);
            debounced_save(frm);
        }
    },
    
    onload: function(frm) {
        // Setup mermaid configuration
        if (typeof mermaid !== 'undefined') {
            mermaid.initialize({
                startOnLoad: false,
                theme: 'default',
                securityLevel: 'loose',
                flowchart: {
                    useMaxWidth: true,
                    htmlLabels: true
                }
            });
        }
    }
});

function setup_realtime_sync(frm) {
    if (!frm.doc.name) return;
    
    // Join the document room for real-time updates
    frappe.realtime.on(`mermaid_diagram_updated`, function(data) {
        if (data.name === frm.doc.name && data.modified !== frm.doc.modified) {
            // Update content without triggering events
            frm.set_value('mermaid_content', data.content, false, true);
            frm.set_value('rendered_svg', data.rendered_svg, false, true);
            
            // Re-render preview
            render_mermaid_preview(frm);
            
            frappe.show_alert({
                message: __('Diagram updated by another user'),
                indicator: 'blue'
            });
        }
    });
}

function render_mermaid_preview(frm) {
    if (!frm.doc.mermaid_content || typeof mermaid === 'undefined') return;
    
    const preview_id = 'mermaid-preview-' + Math.random().toString(36).substr(2, 9);
    
    // Create or update preview container
    let preview_container = frm.fields_dict.mermaid_content.$wrapper.find('.mermaid-preview');
    if (!preview_container.length) {
        preview_container = $(`
            <div class="mermaid-preview" style="
                margin-top: 10px; 
                padding: 15px; 
                border: 1px solid #d1d8dd; 
                border-radius: 4px;
                background: white;
                overflow: auto;
                max-height: 400px;
            ">
                <div class="preview-header" style="margin-bottom: 10px; font-weight: bold;">
                    Live Preview
                </div>
                <div id="${preview_id}" class="mermaid-diagram"></div>
            </div>
        `);
        frm.fields_dict.mermaid_content.$wrapper.append(preview_container);
    } else {
        preview_container.find('.mermaid-diagram').attr('id', preview_id);
    }
    
    // Render the diagram
    try {
        mermaid.render(preview_id + '-svg', frm.doc.mermaid_content, function(svg) {
            preview_container.find('.mermaid-diagram').html(svg);
            
            // Save rendered SVG
            frm.set_value('rendered_svg', svg);
        });
    } catch (error) {
        preview_container.find('.mermaid-diagram').html(`
            <div style="color: red; padding: 10px;">
                <strong>Rendering Error:</strong><br>
                ${error.message}
            </div>
        `);
    }
}

function show_mermaid_preview(frm) {
    if (!frm.doc.mermaid_content) {
        frappe.msgprint(__('No content to preview'));
        return;
    }
    
    const dialog = new frappe.ui.Dialog({
        title: __('Mermaid Preview'),
        size: 'extra-large',
        fields: [
            {
                fieldtype: 'HTML',
                fieldname: 'preview_html'
            }
        ]
    });
    
    const preview_id = 'dialog-mermaid-' + Math.random().toString(36).substr(2, 9);
    dialog.fields_dict.preview_html.$wrapper.html(`
        <div style="text-align: center; padding: 20px;">
            <div id="${preview_id}"></div>
        </div>
    `);
    
    dialog.show();
    
    // Render in dialog
    try {
        mermaid.render(preview_id + '-svg', frm.doc.mermaid_content, function(svg) {
            dialog.fields_dict.preview_html.$wrapper.find(`#${preview_id}`).html(svg);
        });
    } catch (error) {
        dialog.fields_dict.preview_html.$wrapper.find(`#${preview_id}`).html(`
            <div style="color: red;">Error rendering diagram: ${error.message}</div>
        `);
    }
}

// Debounced functions to prevent excessive API calls
const debounced_render = frappe.utils.debounce(render_mermaid_preview, 1000);
const debounced_save = frappe.utils.debounce(function(frm) {
    if (frm.doc.__unsaved) {
        frm.save();
    }
}, 2000);