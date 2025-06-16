// Initialize mermaid with default settings
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
}
