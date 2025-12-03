import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:provider/provider.dart';
import '../utils/constants.dart';
import '../models/meal.dart';
import '../services/user_provider.dart';

class MealPlanScreen extends StatefulWidget {
  const MealPlanScreen({super.key});

  @override
  State<MealPlanScreen> createState() => _MealPlanScreenState();
}

class _MealPlanScreenState extends State<MealPlanScreen> {
  int _selectedDayIndex = 0;
  final List<String> _daysOfWeek = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday',
  ];

  // Sample meal data - in a real app, this would come from the backend
  List<DayMealPlan> _generateMealPlans() {
    return _daysOfWeek.map((day) {
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
  }

  @override
  Widget build(BuildContext context) {
    final userProvider = context.watch<UserProvider>();
    final providerPlans = userProvider.samplePlans;
    final mealPlans = (providerPlans.isNotEmpty)
        ? providerPlans
        : _generateMealPlans();
    final selectedPlan = mealPlans[_selectedDayIndex];
    final dailyCalories = userProvider.profile.dailyCalories ?? 2000;

    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Column(
          children: [
            // Header
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [
                    AppColors.primary,
                    AppColors.primary.withOpacity(0.8),
                  ],
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                        children: [
                          const Icon(
                            Icons.calendar_today,
                            color: Colors.white,
                            size: 28,
                          ),
                          const SizedBox(width: 12),
                          const Text(
                            'Weekly Meal Plan',
                            style: TextStyle(
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                          const Spacer(),
                          IconButton(
                            icon: const Icon(
                              Icons.settings,
                              color: Colors.white,
                            ),
                            onPressed: () {
                              // Settings or profile edit
                            },
                          ),
                        ],
                      )
                      .animate()
                      .fadeIn(delay: 200.ms, duration: 600.ms)
                      .slideY(begin: -0.3, end: 0),
                  const SizedBox(height: 16),
                  // Daily target
                  Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceAround,
                          children: [
                            _buildTargetItem(
                              'Calories',
                              dailyCalories.toStringAsFixed(0),
                              'kcal',
                            ),
                            _buildTargetItem(
                              'Protein',
                              (userProvider.profile.protein ?? 0)
                                  .toStringAsFixed(0),
                              'g',
                            ),
                            _buildTargetItem(
                              'Carbs',
                              (userProvider.profile.carbs ?? 0).toStringAsFixed(
                                0,
                              ),
                              'g',
                            ),
                            _buildTargetItem(
                              'Fats',
                              (userProvider.profile.fats ?? 0).toStringAsFixed(
                                0,
                              ),
                              'g',
                            ),
                          ],
                        ),
                      )
                      .animate()
                      .fadeIn(delay: 400.ms, duration: 600.ms)
                      .slideY(begin: 0.3, end: 0),
                ],
              ),
            ),
            // Day selector
            Container(
              height: 80,
              padding: const EdgeInsets.symmetric(vertical: 12),
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 16),
                itemCount: _daysOfWeek.length,
                itemBuilder: (context, index) {
                  final isSelected = index == _selectedDayIndex;
                  return GestureDetector(
                        onTap: () {
                          setState(() {
                            _selectedDayIndex = index;
                          });
                        },
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 200),
                          margin: const EdgeInsets.only(right: 12),
                          padding: const EdgeInsets.symmetric(
                            horizontal: 20,
                            vertical: 12,
                          ),
                          decoration: BoxDecoration(
                            color: isSelected
                                ? AppColors.primary
                                : Colors.white,
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(
                              color: isSelected
                                  ? AppColors.primary
                                  : AppColors.border,
                            ),
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text(
                                _daysOfWeek[index].substring(0, 3),
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.w600,
                                  color: isSelected
                                      ? Colors.white
                                      : AppColors.textPrimary,
                                ),
                              ),
                            ],
                          ),
                        ),
                      )
                      .animate()
                      .fadeIn(delay: (600 + index * 50).ms, duration: 400.ms)
                      .slideX(begin: -0.2, end: 0);
                },
              ),
            ),
            // Meals list
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.all(24),
                itemCount: selectedPlan.meals.length,
                itemBuilder: (context, index) {
                  final meal = selectedPlan.meals[index];
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 16),
                    child: _buildMealCard(meal)
                        .animate()
                        .fadeIn(delay: (200 + index * 100).ms, duration: 600.ms)
                        .slideX(begin: -0.2, end: 0)
                        .scale(
                          begin: const Offset(0.95, 0.95),
                          end: const Offset(1, 1),
                        ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTargetItem(String label, String value, String unit) {
    return Column(
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 12, color: Colors.white70),
        ),
        const SizedBox(height: 4),
        Row(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Text(
              value,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            const SizedBox(width: 2),
            Text(
              unit,
              style: const TextStyle(fontSize: 12, color: Colors.white70),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildMealCard(Meal meal) {
    IconData icon;
    Color color;

    switch (meal.type.toLowerCase()) {
      case 'breakfast':
        icon = Icons.free_breakfast;
        color = const Color(0xFFFFA726);
      case 'lunch':
        icon = Icons.lunch_dining;
        color = const Color(0xFF66BB6A);
      case 'dinner':
        icon = Icons.dinner_dining;
        color = const Color(0xFF42A5F5);
      default:
        icon = Icons.restaurant;
        color = const Color(0xFFAB47BC);
    }

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Icon(icon, color: color, size: 24),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      meal.type,
                      style: TextStyle(
                        fontSize: 12,
                        color: color,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      meal.name,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                        color: AppColors.textPrimary,
                      ),
                    ),
                  ],
                ),
              ),
              Text(
                '${meal.calories.toInt()} kcal',
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: AppColors.primary,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          // Macros
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildMacroItem(
                'Protein',
                meal.protein.toInt(),
                const Color(0xFFFF6B6B),
              ),
              Container(width: 1, height: 30, color: AppColors.border),
              _buildMacroItem(
                'Carbs',
                meal.carbs.toInt(),
                const Color(0xFF4ECDC4),
              ),
              Container(width: 1, height: 30, color: AppColors.border),
              _buildMacroItem(
                'Fats',
                meal.fats.toInt(),
                const Color(0xFFFFA726),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildMacroItem(String label, int value, Color color) {
    return Column(
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 12, color: AppColors.textSecondary),
        ),
        const SizedBox(height: 4),
        Text(
          '${value}g',
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            color: color,
          ),
        ),
      ],
    );
  }
}
