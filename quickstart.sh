#!/bin/bash

# SQL AI Agent - Quick Start Script
# Makes setup process easier

echo "🚀 SQL AI Agent - Quick Start"
echo "================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found!"
    echo "   Creating from template..."
    cp .env.example .env
    echo ""
    echo "⚙️  Please edit .env and add your API key:"
    echo "   - For OpenAI: Add OPENAI_API_KEY"
    echo "   - For Anthropic: Add ANTHROPIC_API_KEY"
    echo ""
    echo "   Then run this script again."
    exit 1
fi

# Check if API key is set
if ! grep -q "sk-" .env; then
    echo ""
    echo "⚠️  API key not configured in .env file!"
    echo "   Please add your OpenAI or Anthropic API key"
    echo "   Then run this script again."
    exit 1
fi

echo "✅ Configuration found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Check if database exists
if [ ! -f "data/ecommerce.db" ]; then
    echo "🗄️  Database not found. Setting up..."
    echo ""

    # Check if CSV files exist
    if [ ! -d "data/raw" ] || [ -z "$(ls -A data/raw/*.csv 2>/dev/null)" ]; then
        echo "📥 No dataset found. Options:"
        echo ""
        echo "1. Auto-download (requires Kaggle API setup)"
        echo "2. Manual download"
        echo ""
        read -p "Choose option (1/2): " choice

        if [ "$choice" = "1" ]; then
            # Check for Kaggle credentials
            if [ ! -f "$HOME/.kaggle/kaggle.json" ]; then
                echo ""
                echo "❌ Kaggle credentials not found!"
                echo ""
                echo "Setup instructions:"
                echo "1. Go to https://www.kaggle.com/settings"
                echo "2. Click 'Create New API Token'"
                echo "3. Save kaggle.json to ~/.kaggle/"
                echo "4. Run: chmod 600 ~/.kaggle/kaggle.json"
                echo ""
                echo "Then run this script again."
                exit 1
            fi

            echo "📥 Downloading dataset..."
            python src/download_dataset.py

            if [ $? -ne 0 ]; then
                echo "❌ Download failed. Try manual download instead."
                exit 1
            fi
        else
            echo ""
            echo "📋 Manual download instructions:"
            echo "1. Visit: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce"
            echo "2. Download the dataset"
            echo "3. Extract all CSV files to data/raw/ folder"
            echo "4. Run this script again"
            exit 1
        fi
    fi

    # Set up database
    echo ""
    echo "🗄️  Creating database..."
    python src/setup_database.py

    if [ $? -ne 0 ]; then
        echo "❌ Database setup failed!"
        exit 1
    fi
else
    echo "✅ Database found"
fi

echo ""
echo "================================"
echo "✅ Setup complete!"
echo "================================"
echo ""
echo "🚀 Starting application..."
echo ""
echo "The app will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

# Launch Streamlit
streamlit run src/app.py
