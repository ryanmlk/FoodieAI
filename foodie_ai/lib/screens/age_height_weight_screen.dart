import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:provider/provider.dart';
import '../utils/constants.dart';
import '../widgets/custom_button.dart';
import '../widgets/custom_text_field.dart';
import '../services/user_provider.dart';
import 'activity_level_screen.dart';

class AgeHeightWeightScreen extends StatefulWidget {
  const AgeHeightWeightScreen({super.key});

  @override
  State<AgeHeightWeightScreen> createState() => _AgeHeightWeightScreenState();
}

class _AgeHeightWeightScreenState extends State<AgeHeightWeightScreen> {
  final _formKey = GlobalKey<FormState>();
  final _ageController = TextEditingController();
  final _heightController = TextEditingController();
  final _weightController = TextEditingController();

  @override
  void dispose() {
    _ageController.dispose();
    _heightController.dispose();
    _weightController.dispose();
    super.dispose();
  }

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
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Progress indicator
                LinearProgressIndicator(
                  value: 0.4,
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
                  'Tell us about yourself',
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
                  'We need these details to personalize your plan',
                  style: const TextStyle(
                    fontSize: 16,
                    color: AppColors.textSecondary,
                  ),
                )
                    .animate()
                    .fadeIn(delay: 300.ms, duration: 600.ms)
                    .slideY(begin: 0.3, end: 0),
                const SizedBox(height: 40),
                // Input fields
                Expanded(
                  child: ListView(
                    children: [
                      CustomTextField(
                        label: 'Age',
                        hint: 'Enter your age',
                        suffix: 'years',
                        controller: _ageController,
                        keyboardType: TextInputType.number,
                        inputFormatters: [
                          FilteringTextInputFormatter.digitsOnly,
                        ],
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter your age';
                          }
                          final age = int.tryParse(value);
                          if (age == null || age < 10 || age > 120) {
                            return 'Please enter a valid age';
                          }
                          return null;
                        },
                      )
                          .animate()
                          .fadeIn(delay: 400.ms, duration: 600.ms)
                          .slideX(begin: -0.2, end: 0),
                      const SizedBox(height: 24),
                      CustomTextField(
                        label: 'Height',
                        hint: 'Enter your height',
                        suffix: 'cm',
                        controller: _heightController,
                        keyboardType: TextInputType.number,
                        inputFormatters: [
                          FilteringTextInputFormatter.digitsOnly,
                        ],
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter your height';
                          }
                          final height = int.tryParse(value);
                          if (height == null || height < 100 || height > 250) {
                            return 'Please enter a valid height';
                          }
                          return null;
                        },
                      )
                          .animate()
                          .fadeIn(delay: 500.ms, duration: 600.ms)
                          .slideX(begin: -0.2, end: 0),
                      const SizedBox(height: 24),
                      CustomTextField(
                        label: 'Weight',
                        hint: 'Enter your weight',
                        suffix: 'kg',
                        controller: _weightController,
                        keyboardType:
                            const TextInputType.numberWithOptions(decimal: true),
                        inputFormatters: [
                          FilteringTextInputFormatter.allow(
                              RegExp(r'^\d+\.?\d{0,1}')),
                        ],
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter your weight';
                          }
                          final weight = double.tryParse(value);
                          if (weight == null || weight < 30 || weight > 300) {
                            return 'Please enter a valid weight';
                          }
                          return null;
                        },
                      )
                          .animate()
                          .fadeIn(delay: 600.ms, duration: 600.ms)
                          .slideX(begin: -0.2, end: 0),
                    ],
                  ),
                ),
                // Continue button
                CustomButton(
                  text: 'Continue',
                  onPressed: () {
                    if (_formKey.currentState!.validate()) {
                      final userProvider = context.read<UserProvider>();
                      userProvider.updateAge(int.parse(_ageController.text));
                      userProvider
                          .updateHeight(double.parse(_heightController.text));
                      userProvider
                          .updateWeight(double.parse(_weightController.text));

                      Navigator.of(context).push(
                        PageRouteBuilder(
                          pageBuilder: (context, animation, secondaryAnimation) =>
                              const ActivityLevelScreen(),
                          transitionsBuilder:
                              (context, animation, secondaryAnimation, child) {
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
                    }
                  },
                )
                    .animate()
                    .fadeIn(delay: 700.ms, duration: 600.ms)
                    .slideY(begin: 0.3, end: 0),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
