class Meal {
  final String name;
  final String type; // breakfast, lunch, dinner, snack
  final double calories;
  final double protein;
  final double carbs;
  final double fats;

  Meal({
    required this.name,
    required this.type,
    required this.calories,
    required this.protein,
    required this.carbs,
    required this.fats,
  });

  factory Meal.fromJson(Map<String, dynamic> json) => Meal(
    name: json['name'] ?? '',
    type: json['type'] ?? '',
    calories: (json['calories'] ?? 0).toDouble(),
    protein: (json['protein'] ?? 0).toDouble(),
    carbs: (json['carbs'] ?? 0).toDouble(),
    fats: (json['fats'] ?? 0).toDouble(),
  );

  Map<String, dynamic> toJson() => {
    'name': name,
    'type': type,
    'calories': calories,
    'protein': protein,
    'carbs': carbs,
    'fats': fats,
  };
}

class DayMealPlan {
  final String day;
  final List<Meal> meals;

  DayMealPlan({required this.day, required this.meals});

  double get totalCalories => meals.fold(0, (sum, meal) => sum + meal.calories);
  double get totalProtein => meals.fold(0, (sum, meal) => sum + meal.protein);
  double get totalCarbs => meals.fold(0, (sum, meal) => sum + meal.carbs);
  double get totalFats => meals.fold(0, (sum, meal) => sum + meal.fats);
}
