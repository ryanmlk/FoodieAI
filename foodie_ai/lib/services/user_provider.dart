import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/user_profile.dart';
import '../models/meal.dart';

class UserProvider extends ChangeNotifier {
  UserProfile _profile = UserProfile();

  UserProfile get profile => _profile;

  // Helper to get the correct base URL
  String get _baseUrl {
    if (kIsWeb) {
      return 'http://localhost:8000/api/v1';
    }
    // Android emulator needs 10.0.2.2 to access host localhost
    if (Platform.isAndroid) {
      return 'http://10.0.2.2:8000/api/v1';
    }
    // iOS simulator and desktop
    return 'http://localhost:8000/api/v1';
  }

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

  Future<void> calculateNutrition() async {
    // Require core fields
    if (_profile.gender == null ||
        _profile.age == null ||
        _profile.height == null ||
        _profile.weight == null) {
      debugPrint('UserProvider.calculateNutrition: missing required fields');
      return;
    }

    try {
      final url = Uri.parse('$_baseUrl/nutrition/calculate');
      final body = {
        'gender': _profile.gender!.toLowerCase(),
        'age': _profile.age,
        'height': _profile.height,
        'weight': _profile.weight,
        'activity_level': (_profile.activityLevel ?? 'sedentary').toLowerCase(),
        'dietary_preference': (_profile.dietaryPreference ?? 'balanced').toLowerCase(),
      };

      debugPrint('Calling API: $url with body: $body');

      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _profile.dailyCalories = (data['daily_calories'] as num).toDouble();
        _profile.protein = (data['protein'] as num).toDouble();
        _profile.carbs = (data['carbs'] as num).toDouble();
        _profile.fats = (data['fats'] as num).toDouble();
        
        notifyListeners();
        
        // Also fetch the meal plan once nutrition is calculated
        await _fetchMealPlan(body);
        
      } else {
        debugPrint('Failed to calculate nutrition: ${response.statusCode}');
        debugPrint('Response: ${response.body}');
      }
    } catch (e) {
      debugPrint('Error calculating nutrition: $e');
    }
  }

  Future<void> _fetchMealPlan(Map<String, dynamic> requestBody) async {
    try {
      final url = Uri.parse('$_baseUrl/nutrition/meal-plan');
      
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(requestBody),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final items = data['items'] as List;
        
        _samplePlans = items.map((item) {
          final mealsList = (item['meals'] as List).map((m) {
            return Meal(
              name: m['name'],
              type: m['type'],
              calories: (m['calories'] as num).toDouble(), // Changed to double as per model
              protein: (m['protein'] as num).toDouble(),
              carbs: (m['carbs'] as num).toDouble(),
              fats: (m['fats'] as num).toDouble(),
            );
          }).toList();
          
          return DayMealPlan(
            day: item['day'],
            meals: mealsList,
          );
        }).toList();

        notifyListeners();
      } else {
        debugPrint('Failed to fetch meal plan: ${response.statusCode}');
      }
    } catch (e) {
      debugPrint('Error fetching meal plan: $e');
    }
  }

  void reset() {
    _profile = UserProfile();
    notifyListeners();
  }

  List<DayMealPlan> _samplePlans = [];

  List<DayMealPlan> get samplePlans => _samplePlans;

  void populateSampleMealPlans() {
    // No-op, handled in _fetchMealPlan
  }
}
