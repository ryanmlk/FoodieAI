from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserProfileRequest, NutritionGoalsResponse
from app.schemas.meal_schema import MealPlanResponse
from app.services.nutrition_analyzer import NutritionAnalyzer
from app.services.meal_planner import MealPlanner

router = APIRouter(
    prefix="/nutrition",
    tags=["nutrition"]
)

@router.post("/calculate", response_model=NutritionGoalsResponse)
async def calculate_nutrition(profile: UserProfileRequest):
    try:
        result = NutritionAnalyzer.calculate_goals(profile)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/meal-plan", response_model=MealPlanResponse)
async def generate_meal_plan(profile: UserProfileRequest):
    # We pass the profile to the meal planner to get the calories context
    # though the simple mock currently just returns static data.
    try:
        goals = NutritionAnalyzer.calculate_goals(profile)
        plan = MealPlanner.generate_plan(
            calorie_target=goals.daily_calories,
            diet_type=profile.dietary_preference
        )
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
