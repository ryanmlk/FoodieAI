import 'package:flutter/foundation.dart';
import '../models/user_profile.dart';
import '../models/meal.dart';

class UserProvider extends ChangeNotifier {
  UserProfile _profile = UserProfile();

  UserProfile get profile => _profile;

  void updateGender(String gender) {
    _profile.gender = gender;
    notifyListeners();
  }

  void updateAge(int age) {
    _profile.age = age;
    notifyListeners();
  }

  void updateHeight(double height) {
    _profile.height = height;
    notifyListeners();
  }

  void updateWeight(double weight) {
    _profile.weight = weight;
    notifyListeners();
  }

  void updateActivityLevel(String level) {
    _profile.activityLevel = level;
    notifyListeners();
  }

  void updateDietaryPreference(String preference) {
    _profile.dietaryPreference = preference;
    notifyListeners();
  }

  void calculateNutrition() {
    // Require core fields; dietaryPreference and activityLevel can default
    if (_profile.gender == null ||
        _profile.age == null ||
        _profile.height == null ||
        _profile.weight == null) {
      debugPrint('UserProvider.calculateNutrition: missing required fields');
      return;
    }

    // normalize inputs
    final gender = _profile.gender!.toLowerCase();
    final age = _profile.age!;
    final height = _profile.height!;
    final weight = _profile.weight!;

    // Calculate BMR using Mifflin-St Jeor Equation
    double bmr;
    if (gender == 'male' || gender == 'm') {
      bmr = 10 * weight + 6.25 * height - 5 * age + 5;
    } else {
      // treat anything else as female for the formula fallback
      bmr = 10 * weight + 6.25 * height - 5 * age - 161;
    }

    // Apply activity multiplier (default to sedentary if missing)
    final activity = (_profile.activityLevel ?? 'sedentary').toLowerCase();
    double activityMultiplier;
    switch (activity) {
      case 'sedentary':
        activityMultiplier = 1.2;
        break;
      case 'light':
        activityMultiplier = 1.375;
        break;
      case 'moderate':
        activityMultiplier = 1.55;
        break;
      case 'very':
        activityMultiplier = 1.725;
        break;
      case 'extra':
        activityMultiplier = 1.9;
        break;
      default:
        activityMultiplier = 1.2;
    }

    _profile.dailyCalories = bmr * activityMultiplier;

    // Calculate macros based on dietary preference (default to balanced)
    final pref = (_profile.dietaryPreference ?? 'balanced').toLowerCase();
    switch (pref) {
      case 'keto':
        _profile.protein = _profile.dailyCalories! * 0.25 / 4; // 25% protein
        _profile.carbs = _profile.dailyCalories! * 0.05 / 4; // 5% carbs
        _profile.fats = _profile.dailyCalories! * 0.70 / 9; // 70% fats
        break;
      case 'vegan':
      case 'vegetarian':
        _profile.protein = _profile.dailyCalories! * 0.20 / 4; // 20% protein
        _profile.carbs = _profile.dailyCalories! * 0.55 / 4; // 55% carbs
        _profile.fats = _profile.dailyCalories! * 0.25 / 9; // 25% fats
        break;
      default: // balanced
        _profile.protein = _profile.dailyCalories! * 0.30 / 4; // 30% protein
        _profile.carbs = _profile.dailyCalories! * 0.40 / 4; // 40% carbs
        _profile.fats = _profile.dailyCalories! * 0.30 / 9; // 30% fats
    }

    notifyListeners();
  }

  void reset() {
    _profile = UserProfile();
    notifyListeners();
  }

  // Simple in-memory sample meal plans to use until backend is connected.
  List<DayMealPlan> _samplePlans = [];

  List<DayMealPlan> get samplePlans => _samplePlans;

  void populateSampleMealPlans() {
    // Create a simple 7-day plan with placeholder meals.
    final days = [
      'Monday',
      'Tuesday',
      'Wednesday',
      'Thursday',
      'Friday',
      'Saturday',
      'Sunday',
    ];

    _samplePlans = days.map((day) {
      return DayMealPlan(
        day: day,
        meals: [
          Meal(
            name: 'Oatmeal with Berries',
            type: 'Breakfast',
            calories: 350,
            protein: 12,
            carbs: 58,
            fats: 8,
          ),
          Meal(
            name: 'Grilled Chicken Salad',
            type: 'Lunch',
            calories: 450,
            protein: 35,
            carbs: 25,
            fats: 18,
          ),
          Meal(
            name: 'Salmon with Vegetables',
            type: 'Dinner',
            calories: 550,
            protein: 42,
            carbs: 35,
            fats: 22,
          ),
          Meal(
            name: 'Greek Yogurt',
            type: 'Snack',
            calories: 150,
            protein: 15,
            carbs: 12,
            fats: 4,
          ),
        ],
      );
    }).toList();

    notifyListeners();
  }
}
