# 🚀 Quick Start Guide - FoodieAI

## Prerequisites

- Flutter SDK (>=3.9.2)
- A device or emulator to run the app

## Installation & Running

### Method 1: Using the Shell Script (Recommended)

```bash
cd /mnt/area51/Projects/FoodieAI/foodie_ai
./run_app.sh
```

The script will:
1. Check if Flutter is installed
2. Install all dependencies
3. Launch the app on Linux

### Method 2: Manual Installation

```bash
# Navigate to the project
cd /mnt/area51/Projects/FoodieAI/foodie_ai

# Get dependencies
flutter pub get

# Run the app
flutter run -d linux
```

### Running on Different Platforms

**Web:**
```bash
flutter run -d chrome
```

**Android:**
```bash
flutter run -d android
```

**iOS:**
```bash
flutter run -d ios
```

**List available devices:**
```bash
flutter devices
```

## 🎯 Using the App

1. **Welcome Screen**
   - Tap "Get Started" to begin

2. **Gender Selection**
   - Choose your gender (Male/Female)
   - Tap "Continue"

3. **Personal Information**
   - Enter your age (years)
   - Enter your height (cm)
   - Enter your weight (kg)
   - Tap "Continue"

4. **Activity Level**
   - Select your activity level (from Sedentary to Extra Active)
   - Tap "Continue"

5. **Dietary Preference**
   - Choose your dietary style (Balanced, Vegetarian, Vegan, or Keto)
   - Tap "Calculate My Plan"

6. **View Results**
   - See your calculated daily calorie goal
   - View your macro breakdown (Protein, Carbs, Fats)
   - Tap "View Weekly Meal Plan"

7. **Weekly Meal Plan**
   - Swipe through days of the week
   - View meals for each day
   - See nutritional information for each meal

## 📁 Project Structure

```
foodie_ai/
├── lib/
│   ├── main.dart                    # App entry point
│   ├── models/                      # Data models
│   ├── screens/                     # All UI screens
│   ├── widgets/                     # Reusable components
│   ├── services/                    # State management & logic
│   └── utils/                       # Constants & utilities
├── assets/
│   └── images/                      # Image assets
├── pubspec.yaml                     # Dependencies
├── README.md                        # Project documentation
├── FEATURES.md                      # Detailed features list
└── run_app.sh                       # Launch script
```

## 🎨 Key Features

✅ Beautiful animated onboarding flow
✅ Smart nutritional calculations based on BMR
✅ Personalized macronutrient distribution
✅ Weekly meal planning interface
✅ Smooth transitions and animations
✅ Material Design 3 UI
✅ Responsive layout

## 🔧 Troubleshooting

### Dependencies not installing
```bash
flutter clean
flutter pub get
```

### App not running
```bash
flutter doctor
```
Check for any issues with your Flutter installation.

### Hot reload not working
Press `r` in the terminal while the app is running, or use the hot reload button in your IDE.

## 📝 Development

### Adding new dependencies
1. Add to `pubspec.yaml`
2. Run `flutter pub get`

### Running tests
```bash
flutter test
```

### Building for release
```bash
# Android
flutter build apk --release

# iOS
flutter build ios --release

# Web
flutter build web --release
```

## 🎯 Next Steps

1. **Backend Integration**: Connect to the Python FastAPI server at `/backend`
2. **Real Data**: Replace sample meals with actual database queries
3. **Persistence**: Save user profiles using SharedPreferences
4. **Additional Features**: Add grocery lists, recipe details, etc.

## 📚 Resources

- [Flutter Documentation](https://flutter.dev/docs)
- [Material Design 3](https://m3.material.io/)
- [Flutter Animate Package](https://pub.dev/packages/flutter_animate)
- [Provider Package](https://pub.dev/packages/provider)

## 🆘 Need Help?

- Check the error console for detailed error messages
- Review `FEATURES.md` for complete feature documentation
- Ensure all dependencies are properly installed
- Make sure you're using Flutter SDK >=3.9.2

## 🎉 Enjoy using FoodieAI!
