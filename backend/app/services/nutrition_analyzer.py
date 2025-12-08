from app.schemas.user_schema import UserProfileRequest, NutritionGoalsResponse, Gender, ActivityLevel, DietaryPreference

class NutritionAnalyzer:
    @staticmethod
    def calculate_goals(profile: UserProfileRequest) -> NutritionGoalsResponse:
        # 1. Calculate BMR (Mifflin-St Jeor)
        # Men: 10W + 6.25H - 5A + 5
        # Women: 10W + 6.25H - 5A - 161
        weight = profile.weight
        height = profile.height
        age = profile.age
        
        if profile.gender == Gender.MALE:
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            # Female or other (defaulting to female formula as per original code)
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
            
        # 2. Activity Multiplier
        activity_map = {
            ActivityLevel.SEDENTARY: 1.2,
            ActivityLevel.LIGHT: 1.375,
            ActivityLevel.MODERATE: 1.55,
            ActivityLevel.VERY: 1.725,
            ActivityLevel.EXTRA: 1.9,
        }
        multiplier = activity_map.get(profile.activity_level, 1.2)
        daily_calories = bmr * multiplier
        
        # 3. Macro Split
        # Default balanced: 30% P, 40% C, 30% F
        # Keto: 25% P, 5% C, 70% F
        # Vegan/Veg: 20% P, 55% C, 25% F
        
        if profile.dietary_preference == DietaryPreference.KETO:
            p_ratio, c_ratio, f_ratio = 0.25, 0.05, 0.70
        elif profile.dietary_preference in [DietaryPreference.VEGAN, DietaryPreference.VEGETARIAN]:
            p_ratio, c_ratio, f_ratio = 0.20, 0.55, 0.25
        else: # Balanced
            p_ratio, c_ratio, f_ratio = 0.30, 0.40, 0.30
            
        protein = (daily_calories * p_ratio) / 4
        carbs = (daily_calories * c_ratio) / 4
        fats = (daily_calories * f_ratio) / 9
        
        return NutritionGoalsResponse(
            daily_calories=daily_calories,
            protein=protein,
            carbs=carbs,
            fats=fats
        )
