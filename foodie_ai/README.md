# FoodieAI - Personalized Meal Planning App

A Flutter application that helps users manage their meal plans by gathering basic information and calculating personalized nutritional goals.

## Features

✅ **Beautiful Onboarding Flow**
- Animated welcome screen with smooth transitions
- Step-by-step user information collection
- Progress indicators showing completion status

✅ **Smart Nutritional Calculation**
- BMR calculation using Mifflin-St Jeor Equation
- Activity level adjustments
- Customized macronutrient distribution based on dietary preferences

✅ **Weekly Meal Planning**
- Day-by-day meal breakdown
- Detailed nutritional information for each meal
- Visual meal cards with icons and colors
- Daily calorie and macro tracking

✅ **Smooth Animations**
- Fade and slide transitions between screens
- Scale animations on cards
- Loading animations during calculations
- Interactive selection feedback

## Screens

1. **Welcome Screen** - App introduction with feature highlights
2. **Gender Selection** - Choose user gender
3. **Personal Info** - Enter age, height, and weight
4. **Activity Level** - Select physical activity level
5. **Dietary Preference** - Choose eating style (Balanced, Vegetarian, Vegan, Keto)
6. **Calculating Screen** - Animated processing screen
7. **Nutrition Results** - Display calculated daily goals
8. **Meal Plan Screen** - Weekly meal plan with detailed breakdown

## Installation

1. Ensure you have Flutter installed (SDK >=3.9.2)
2. Navigate to the project directory:
   ```bash
   cd foodie_ai
   ```
3. Get dependencies:
   ```bash
   flutter pub get
   ```
4. Run the app:
   ```bash
   flutter run
   ```

## Dependencies

- **flutter_animate** - Powerful animation library
- **provider** - State management
- **google_fonts** - Custom fonts (Inter)
- **shared_preferences** - Local data persistence
- **intl** - Internationalization and formatting

## Project Structure

```
lib/
├── main.dart                 # App entry point
├── models/                   # Data models
│   ├── user_profile.dart
│   └── meal.dart
├── screens/                  # All app screens
│   ├── welcome_screen.dart
│   ├── gender_selection_screen.dart
│   ├── age_height_weight_screen.dart
│   ├── activity_level_screen.dart
│   ├── dietary_preference_screen.dart
│   ├── calculating_screen.dart
│   ├── nutrition_results_screen.dart
│   └── meal_plan_screen.dart
├── widgets/                  # Reusable widgets
│   ├── custom_button.dart
│   ├── custom_text_field.dart
│   └── selection_card.dart
├── services/                 # Business logic
│   └── user_provider.dart
└── utils/                    # Constants and utilities
    └── constants.dart
```

## Color Scheme

- **Primary**: #6C63FF (Purple)
- **Secondary**: #FF6584 (Pink)
- **Accent**: #4CAF50 (Green)
- **Background**: #F8F9FA (Light Gray)

## Nutritional Calculation

### BMR Formula (Mifflin-St Jeor)
- **Male**: BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) + 5
- **Female**: BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) - 161

### Activity Multipliers
- Sedentary: 1.2
- Lightly Active: 1.375
- Moderately Active: 1.55
- Very Active: 1.725
- Extra Active: 1.9

### Macronutrient Distribution
- **Balanced**: 30% Protein, 40% Carbs, 30% Fats
- **Keto**: 25% Protein, 5% Carbs, 70% Fats
- **Vegetarian/Vegan**: 20% Protein, 55% Carbs, 25% Fats

## Future Enhancements

- Backend integration with the Python FastAPI server
- Real meal suggestions from the database
- Grocery list generation
- Recipe details and cooking instructions
- Progress tracking and analytics
- Social features and meal sharing
- Barcode scanning for food items
- Integration with fitness trackers

## License

This project is part of the FoodieAI application suite.
