import 'package:flutter/material.dart';

class AppColors {
  static const primary = Color(0xFF6C63FF);
  static const secondary = Color(0xFFFF6584);
  static const accent = Color(0xFF4CAF50);
  static const background = Color(0xFFF8F9FA);
  static const cardBackground = Colors.white;
  static const textPrimary = Color(0xFF2D3748);
  static const textSecondary = Color(0xFF718096);
  static const border = Color(0xFFE2E8F0);
}

class ActivityLevels {
  static const List<Map<String, String>> levels = [
    {
      'value': 'sedentary',
      'label': 'Sedentary',
      'description': 'Little or no exercise',
    },
    {
      'value': 'light',
      'label': 'Lightly Active',
      'description': 'Exercise 1-3 days/week',
    },
    {
      'value': 'moderate',
      'label': 'Moderately Active',
      'description': 'Exercise 3-5 days/week',
    },
    {
      'value': 'very',
      'label': 'Very Active',
      'description': 'Exercise 6-7 days/week',
    },
    {
      'value': 'extra',
      'label': 'Extra Active',
      'description': 'Very intense exercise daily',
    },
  ];
}

class DietaryPreferences {
  static const List<Map<String, String>> preferences = [
    {
      'value': 'balanced',
      'label': 'Balanced',
      'description': 'Mix of all food groups',
    },
    {
      'value': 'vegetarian',
      'label': 'Vegetarian',
      'description': 'No meat, includes dairy & eggs',
    },
    {'value': 'vegan', 'label': 'Vegan', 'description': 'No animal products'},
    {'value': 'keto', 'label': 'Keto', 'description': 'Low carb, high fat'},
  ];
}
