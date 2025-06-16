// Wait for Mermaid to be available
function initializeMermaid() {
    if (window.mermaid) {
        window.mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
            fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
            flowchart: {
                htmlLabels: true,
                curve: 'basis'
            }
        });
    } else {
        setTimeout(initializeMermaid, 100);
    }
}

// Start initialization when script loads
initializeMermaid();
