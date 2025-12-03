import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:provider/provider.dart';
import '../utils/constants.dart';
import '../services/user_provider.dart';
import 'nutrition_results_screen.dart';

class CalculatingScreen extends StatefulWidget {
  const CalculatingScreen({super.key});

  @override
  State<CalculatingScreen> createState() => _CalculatingScreenState();
}

class _CalculatingScreenState extends State<CalculatingScreen> {
  @override
  void initState() {
    super.initState();
    // Defer the heavy work to after the first frame so any notifyListeners
    // calls inside calculation don't run during the widget build phase.
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _performCalculation();
    });
  }

  Future<void> _performCalculation() async {
    // Calculate nutrition
    context.read<UserProvider>().calculateNutrition();

    // Simulate processing time for better UX
    await Future.delayed(const Duration(milliseconds: 2500));

    if (mounted) {
      Navigator.of(context).pushReplacement(
        PageRouteBuilder(
          pageBuilder: (context, animation, secondaryAnimation) =>
              const NutritionResultsScreen(),
          transitionsBuilder: (context, animation, secondaryAnimation, child) {
            return FadeTransition(opacity: animation, child: child);
          },
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.primary,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Animated icon
              Container(
                    width: 120,
                    height: 120,
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(30),
                    ),
                    child: const Icon(
                      Icons.calculate_outlined,
                      size: 60,
                      color: Colors.white,
                    ),
                  )
                  .animate(onPlay: (controller) => controller.repeat())
                  .scale(
                    duration: 1000.ms,
                    begin: const Offset(1.0, 1.0),
                    end: const Offset(1.1, 1.1),
                  )
                  .then()
                  .scale(
                    duration: 1000.ms,
                    begin: const Offset(1.1, 1.1),
                    end: const Offset(1.0, 1.0),
                  ),
              const SizedBox(height: 40),
              // Title
              const Text(
                    'Calculating your\nnutritional goals',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                      height: 1.2,
                    ),
                  )
                  .animate()
                  .fadeIn(delay: 200.ms, duration: 600.ms)
                  .slideY(begin: 0.3, end: 0),
              const SizedBox(height: 16),
              // Subtitle
              const Text(
                    'Personalizing your meal plan based on\nyour profile and preferences',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.white70,
                      height: 1.5,
                    ),
                  )
                  .animate()
                  .fadeIn(delay: 400.ms, duration: 600.ms)
                  .slideY(begin: 0.3, end: 0),
              const SizedBox(height: 60),
              // Progress indicators
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(
                  3,
                  (index) =>
                      Container(
                            margin: const EdgeInsets.symmetric(horizontal: 4),
                            width: 12,
                            height: 12,
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(6),
                            ),
                          )
                          .animate(onPlay: (controller) => controller.repeat())
                          .fadeOut(delay: (index * 200).ms, duration: 600.ms)
                          .then()
                          .fadeIn(duration: 600.ms),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
