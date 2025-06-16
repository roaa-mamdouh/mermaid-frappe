const path = require('path');

module.exports = {
  entryPoints: ['mermaid/public/frontend/src/main.js'],
  bundle: true,
  outfile: 'mermaid/public/mermaid.bundle.js',
  platform: 'browser',
  target: ['es2020'],
  format: 'esm',
  minify: true,
  sourcemap: true,
  loader: {
    '.js': 'jsx',
    '.ts': 'ts',
    '.tsx': 'tsx',
    '.vue': 'vue',
  },
  plugins: [
    {
      name: 'vue-style',
      setup(build) {
        build.onEnd((result) => {
          if (result.metafile && result.metafile.outputs) {
            const files = Object.keys(result.metafile.outputs);
            // Process Vue style files here
          }
        });
      },
    },
  ],
  define: {
    'process.env.NODE_ENV': '"production"',
  },
  external: [
    'vue',
    'frappe-ui',
    'monaco-editor',
    'mermaid',
    'html2canvas',
    'jspdf',
  ],
}; 