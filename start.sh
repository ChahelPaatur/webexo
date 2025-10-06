#!/bin/bash

echo "🌟 Starting ExoML Platform..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "💡 Run './setup.sh' first to install dependencies"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if model files exist
if [ ! -f "model_files/exoplanet_bilstm.h5" ]; then
    echo "❌ Model file not found!"
    echo "💡 Make sure model files are in the 'model_files/' directory"
    exit 1
fi

echo "✓ Model files found"
echo ""

# Start Flask server
echo "🚀 Starting Flask backend server on http://127.0.0.1:5001"
echo ""
echo "📝 To stop the server, press Ctrl+C"
echo "📝 Open index.html in your browser to access the frontend"
echo ""
python app.py

