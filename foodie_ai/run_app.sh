#!/bin/bash

# FoodieAI Flutter App Launch Script

echo "🍔 FoodieAI - Starting the app..."
echo ""

# Check if Flutter is installed
if ! command -v flutter &> /dev/null
then
    echo "❌ Flutter is not installed. Please install Flutter first."
    echo "Visit: https://flutter.dev/docs/get-started/install"
    exit 1
fi

echo "✅ Flutter detected"
echo ""

# Navigate to the foodie_ai directory
cd "$(dirname "$0")"

# Check if we're in the right directory
if [ ! -f "pubspec.yaml" ]; then
    echo "❌ Error: pubspec.yaml not found. Please run this script from the foodie_ai directory."
    exit 1
fi

# Get dependencies
echo "📦 Installing dependencies..."
flutter pub get

if [ $? -ne 0 ]; then
    echo "❌ Failed to get dependencies"
    exit 1
fi

echo ""
echo "✅ Dependencies installed"
echo ""

# Run the app
echo "🚀 Launching FoodieAI..."
echo ""

flutter run -d linux

# If you want to run on a specific device, uncomment one of these:
# flutter run -d chrome      # For web
# flutter run -d android     # For Android
# flutter run -d ios         # For iOS
