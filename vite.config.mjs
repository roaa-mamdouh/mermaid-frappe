import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import Icons from 'unplugin-icons/vite';
import path from 'path';

export default defineConfig({
  root: path.resolve(process.cwd(), 'mermaid/public/frontend'),
  plugins: [
    vue(),
    Icons({
      compiler: 'vue3',
      autoInstall: true,
      scale: 1,
      defaultClass: 'icon',
    }),
  ],
  build: {
    outDir: path.resolve(process.cwd(), 'mermaid/public/frontend/dist'),
    emptyOutDir: true,
    rollupOptions: {
      external: ['mermaid', 'monaco-editor', 'vs/editor/editor.main'],
      output: {
        globals: {
          mermaid: 'mermaid',
          'monaco-editor': 'monaco',
          'vs/editor/editor.main': 'monaco'
        }
      }
    }
  },
  optimizeDeps: {
    exclude: ['monaco-editor']
  }
}); 