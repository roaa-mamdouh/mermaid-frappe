#!/bin/bash

# Mermaid App Build Script
# This script handles building the frontend assets for the Mermaid app

set -e

echo "🚀 Building Mermaid App..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js version 16+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Type checking
echo "🔍 Running type checks..."
npm run type-check

# Build Tailwind CSS
echo "🎨 Building Tailwind CSS..."
npx tailwindcss -i ./mermaid/public/css/tailwind.css -o ./mermaid/public/css/tailwind.min.css --minify

# Build JavaScript bundles
echo "📦 Building JavaScript bundles..."
npm run build

# Copy assets to public directory
echo "📁 Organizing assets..."
mkdir -p mermaid/public/dist

# Verify build output
if [ -f "mermaid/public/js/vendor.bundle.js" ] && [ -f "mermaid/public/js/app.bundle.js" ]; then
    echo "✅ Build completed successfully!"
    echo "📊 Build summary:"
    echo "   - Vendor bundle: $(du -h mermaid/public/js/vendor.bundle.js | cut -f1)"
    echo "   - App bundle: $(du -h mermaid/public/js/app.bundle.js | cut -f1)"
    echo "   - Tailwind CSS: $(du -h mermaid/public/css/tailwind.min.css | cut -f1)"
else
    echo "❌ Build failed! Missing output files."
    exit 1
fi

echo "🎉 Mermaid app build completed!"
echo "💡 Next steps:"
echo "   1. Run 'bench build' to compile Frappe assets"
echo "   2. Run 'bench migrate' to apply database changes"
echo "   3. Restart your Frappe server"
