import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:provider/provider.dart';
import '../utils/constants.dart';
import '../widgets/custom_button.dart';
import '../widgets/selection_card.dart';
import '../services/user_provider.dart';
import 'dietary_preference_screen.dart';

class ActivityLevelScreen extends StatefulWidget {
  const ActivityLevelScreen({super.key});

  @override
  State<ActivityLevelScreen> createState() => _ActivityLevelScreenState();
}

class _ActivityLevelScreenState extends State<ActivityLevelScreen> {
  String? _selectedLevel;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: AppColors.textPrimary),
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Progress indicator
              LinearProgressIndicator(
                value: 0.6,
                backgroundColor: AppColors.border,
                color: AppColors.primary,
                borderRadius: BorderRadius.circular(10),
                minHeight: 6,
              )
                  .animate()
                  .fadeIn(duration: 400.ms)
                  .slideX(begin: -0.2, end: 0),
              const SizedBox(height: 32),
              // Title
              Text(
                'How active are you?',
                style: const TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  color: AppColors.textPrimary,
                ),
              )
                  .animate()
                  .fadeIn(delay: 200.ms, duration: 600.ms)
                  .slideY(begin: 0.3, end: 0),
              const SizedBox(height: 8),
              Text(
                'Your activity level affects your calorie needs',
                style: const TextStyle(
                  fontSize: 16,
                  color: AppColors.textSecondary,
                ),
              )
                  .animate()
                  .fadeIn(delay: 300.ms, duration: 600.ms)
                  .slideY(begin: 0.3, end: 0),
              const SizedBox(height: 40),
              // Activity options
              Expanded(
                child: ListView.builder(
                  itemCount: ActivityLevels.levels.length,
                  itemBuilder: (context, index) {
                    final level = ActivityLevels.levels[index];
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 16),
                      child: SelectionCard(
                        title: level['label']!,
                        description: level['description']!,
                        isSelected: _selectedLevel == level['value'],
                        onTap: () {
                          setState(() {
                            _selectedLevel = level['value'];
                          });
                        },
                      )
                          .animate()
                          .fadeIn(delay: (400 + index * 100).ms, duration: 600.ms)
                          .slideX(begin: -0.2, end: 0),
                    );
                  },
                ),
              ),
              // Continue button
              CustomButton(
                text: 'Continue',
                onPressed: _selectedLevel == null
                    ? () {}
                    : () {
                        context
                            .read<UserProvider>()
                            .updateActivityLevel(_selectedLevel!);
                        Navigator.of(context).push(
                          PageRouteBuilder(
                            pageBuilder:
                                (context, animation, secondaryAnimation) =>
                                    const DietaryPreferenceScreen(),
                            transitionsBuilder: (context, animation,
                                secondaryAnimation, child) {
                              const begin = Offset(1.0, 0.0);
                              const end = Offset.zero;
                              const curve = Curves.easeInOut;
                              var tween = Tween(begin: begin, end: end)
                                  .chain(CurveTween(curve: curve));
                              var offsetAnimation = animation.drive(tween);
                              return SlideTransition(
                                position: offsetAnimation,
                                child: child,
                              );
                            },
                          ),
                        );
                      },
              )
                  .animate()
                  .fadeIn(delay: 900.ms, duration: 600.ms)
                  .slideY(begin: 0.3, end: 0),
            ],
          ),
        ),
      ),
    );
  }
}
