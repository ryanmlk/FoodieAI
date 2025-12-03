class UserProfile {
  String? gender;
  int? age;
  double? height; // in cm
  double? weight; // in kg
  String? activityLevel;
  String? dietaryPreference;
  double? dailyCalories;
  double? protein;
  double? carbs;
  double? fats;

  UserProfile({
    this.gender,
    this.age,
    this.height,
    this.weight,
    this.activityLevel,
    this.dietaryPreference,
    this.dailyCalories,
    this.protein,
    this.carbs,
    this.fats,
  });

  bool get isComplete =>
      gender != null &&
      age != null &&
      height != null &&
      weight != null &&
      activityLevel != null &&
      dietaryPreference != null;

  Map<String, dynamic> toJson() => {
    'gender': gender,
    'age': age,
    'height': height,
    'weight': weight,
    'activityLevel': activityLevel,
    'dietaryPreference': dietaryPreference,
    'dailyCalories': dailyCalories,
    'protein': protein,
    'carbs': carbs,
    'fats': fats,
  };

  factory UserProfile.fromJson(Map<String, dynamic> json) => UserProfile(
    gender: json['gender'],
    age: json['age'],
    height: json['height'],
    weight: json['weight'],
    activityLevel: json['activityLevel'],
    dietaryPreference: json['dietaryPreference'],
    dailyCalories: json['dailyCalories'],
    protein: json['protein'],
    carbs: json['carbs'],
    fats: json['fats'],
  );
}
