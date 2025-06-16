# Mermaid Diagram Editor Installation Guide

## Prerequisites

1. Frappe Framework v14+
2. Node.js 16+ and npm
3. Python 3.10+

## Quick Install

```bash
# Get the app
bench get-app mermaid https://github.com/your-repo/mermaid

# Install app dependencies
cd apps/mermaid
npm install

# Build frontend assets
./build.sh

# Install the app on your site
bench --site your-site install-app mermaid

# Run migrations
bench --site your-site migrate
```

## Manual Installation Steps

If you prefer to install manually or need more control:

1. **Clone the repository:**
   ```bash
   cd bench/apps
   git clone https://github.com/your-repo/mermaid
   ```

2. **Install Node.js dependencies:**
   ```bash
   cd mermaid
   npm install
   ```

3. **Build frontend assets:**
   ```bash
   # Build Tailwind CSS
   npx tailwindcss -i ./mermaid/public/css/tailwind.css -o ./mermaid/public/css/tailwind.min.css --minify

   # Build JavaScript bundles
   npm run build
   ```

4. **Install the app:**
   ```bash
   bench --site your-site install-app mermaid
   ```

5. **Run database migrations:**
   ```bash
   bench --site your-site migrate
   ```

6. **Clear cache and rebuild assets:**
   ```bash
   bench clear-cache
   bench build
   ```

7. **Restart the Frappe server:**
   ```bash
   bench restart
   ```

## Verification

1. Log into your Frappe site
2. Navigate to "Mermaid Diagram" in the desk
3. Create a new diagram to verify the editor loads correctly
4. Test the preview functionality
5. Try saving and exporting a diagram

## Common Issues

### Build Failures

If the build fails:
1. Check Node.js version: `node -v` (should be 16+)
2. Clear node_modules: `rm -rf node_modules`
3. Reinstall dependencies: `npm install`
4. Try building again: `./build.sh`

### Asset Loading Issues

If assets don't load:
1. Clear browser cache
2. Run `bench clear-cache`
3. Run `bench build --force`
4. Restart Frappe server: `bench restart`

### Permission Issues

If you encounter permission errors:
1. Check DocType permissions in Role Manager
2. Verify user roles and permissions
3. Clear user permissions cache: `bench --site your-site clear-cache`

## Development Setup

For development:

1. **Enable developer mode:**
   ```bash
   bench set-config -g developer_mode 1
   ```

2. **Start development server:**
   ```bash
   cd apps/mermaid
   npm run dev
   ```

3. **Watch for changes:**
   ```bash
   # In another terminal
   bench watch
   ```

## Updating

To update the app:

1. **Pull latest changes:**
   ```bash
   cd apps/mermaid
   git pull
   ```

2. **Rebuild assets:**
   ```bash
   ./build.sh
   ```

3. **Run migrations:**
   ```bash
   bench --site your-site migrate
   ```

4. **Restart server:**
   ```bash
   bench restart
   ```

## Support

If you encounter any issues:

1. Check the [troubleshooting guide](README.md#troubleshooting)
2. Search [existing issues](https://github.com/your-repo/mermaid/issues)
3. Post on [Frappe Forum](https://discuss.frappe.io)
4. Create a [new issue](https://github.com/your-repo/mermaid/issues/new)

## License

MIT License - see LICENSE file for details.
