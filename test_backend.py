import sys
import os
# Add backend to path so imports work
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from backend.app.services.nutrition_analyzer import NutritionAnalyzer
from backend.app.schemas.user_schema import UserProfileRequest, Gender, ActivityLevel, DietaryPreference

def test_nutrition_calculation():
    print("Testing Nutrition Calculation...")
    profile = UserProfileRequest(
        gender=Gender.FEMALE,
        age=30,
        height=165,
        weight=60,
        activity_level=ActivityLevel.MODERATE,
        dietary_preference=DietaryPreference.BALANCED
    )
    result = NutritionAnalyzer.calculate_goals(profile)
    print(f"BMR/Calories: {result.daily_calories}")
    print(f"Protein: {result.protein}")
    print(f"Carbs: {result.carbs}")
    print(f"Fats: {result.fats}")
    
    # Expected: 
    # BMR approx: 10*60 + 6.25*165 - 5*30 - 161 = 600 + 1031.25 - 150 - 161 = 1320.25
    # TDEE (Moderate 1.55): 1320.25 * 1.55 = 2046.38
    # Protein (30%): 2046.38 * 0.30 / 4 = 153.48
    
    assert result.daily_calories > 1500
    assert result.protein > 0
    print("Nutrition Calculation OK!")

if __name__ == "__main__":
    test_nutrition_calculation()
