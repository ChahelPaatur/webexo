#!/bin/bash

echo "🚀 ExoML Setup Script"
echo "====================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start the Flask server:"
echo "   python app.py"
echo ""
echo "3. Open index.html in your browser"
echo ""
echo "4. Test the API (optional):"
echo "   python test_api.py"
echo ""

