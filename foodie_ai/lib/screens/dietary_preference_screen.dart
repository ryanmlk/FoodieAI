import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:provider/provider.dart';
import '../utils/constants.dart';
import '../widgets/custom_button.dart';
import '../widgets/selection_card.dart';
import '../services/user_provider.dart';
import 'calculating_screen.dart';

class DietaryPreferenceScreen extends StatefulWidget {
  const DietaryPreferenceScreen({super.key});

  @override
  State<DietaryPreferenceScreen> createState() =>
      _DietaryPreferenceScreenState();
}

class _DietaryPreferenceScreenState extends State<DietaryPreferenceScreen> {
  String? _selectedPreference;

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
                value: 0.8,
                backgroundColor: AppColors.border,
                color: AppColors.primary,
                borderRadius: BorderRadius.circular(10),
                minHeight: 6,
              ).animate().fadeIn(duration: 400.ms).slideX(begin: -0.2, end: 0),
              const SizedBox(height: 32),
              // Title
              Text(
                    'Dietary preference',
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
                    'Choose your preferred eating style',
                    style: const TextStyle(
                      fontSize: 16,
                      color: AppColors.textSecondary,
                    ),
                  )
                  .animate()
                  .fadeIn(delay: 300.ms, duration: 600.ms)
                  .slideY(begin: 0.3, end: 0),
              const SizedBox(height: 40),
              // Dietary options
              Expanded(
                child: ListView.builder(
                  itemCount: DietaryPreferences.preferences.length,
                  itemBuilder: (context, index) {
                    final pref = DietaryPreferences.preferences[index];
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 16),
                      child:
                          SelectionCard(
                                title: pref['label']!,
                                description: pref['description']!,
                                isSelected:
                                    _selectedPreference == pref['value'],
                                onTap: () {
                                  setState(() {
                                    _selectedPreference = pref['value'];
                                  });
                                },
                              )
                              .animate()
                              .fadeIn(
                                delay: (400 + index * 100).ms,
                                duration: 600.ms,
                              )
                              .slideX(begin: -0.2, end: 0),
                    );
                  },
                ),
              ),
              // Continue button
              CustomButton(
                text: 'Calculate My Plan',
                onPressed: _selectedPreference == null
                    ? () {}
                    : () {
                        final provider = context.read<UserProvider>();
                        // update preference and populate sample plans immediately
                        provider.updateDietaryPreference(_selectedPreference!);
                        provider.populateSampleMealPlans();

                        // Schedule navigation after this frame to avoid calling
                        // notifyListeners() during the build phase (fixes the
                        // FlutterError: setState() or markNeedsBuild() called during build).
                        WidgetsBinding.instance.addPostFrameCallback((_) {
                          Navigator.of(context).push(
                            PageRouteBuilder(
                              pageBuilder:
                                  (context, animation, secondaryAnimation) =>
                                      const CalculatingScreen(),
                              transitionsBuilder:
                                  (
                                    context,
                                    animation,
                                    secondaryAnimation,
                                    child,
                                  ) {
                                    return FadeTransition(
                                      opacity: animation,
                                      child: child,
                                    );
                                  },
                            ),
                          );
                        });
                      },
              ).animate().fadeIn(delay: 800.ms, duration: 600.ms).slideY(begin: 0.3, end: 0),
            ],
          ),
        ),
      ),
    );
  }
}
