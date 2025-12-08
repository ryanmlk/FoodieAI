from typing import List
from app.schemas.meal_schema import Meal, DayMealPlan, MealPlanResponse

class MealPlanner:
    @staticmethod
    def generate_plan(calorie_target: float, diet_type: str = "balanced") -> MealPlanResponse:
        # NOTE: This is a static/mock implementation to match the current Flutter prototype.
        # In a real system, this would query a database or use an optimization algorithm
        # to find meals matching the calorie_target and diet_type.
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Scaling factor could be applied here if we had real recipes
        
        daily_plans = []
        for day in days:
            meals = [
                Meal(
                    name='Oatmeal with Berries',
                    type='Breakfast',
                    calories=350,
                    protein=12,
                    carbs=58,
                    fats=8
                ),
                Meal(
                    name='Grilled Chicken Salad',
                    type='Lunch',
                    calories=450,
                    protein=35,
                    carbs=25,
                    fats=18
                ),
                Meal(
                    name='Salmon with Vegetables',
                    type='Dinner',
                    calories=550,
                    protein=42,
                    carbs=35,
                    fats=22
                ),
                Meal(
                    name='Greek Yogurt',
                    type='Snack',
                    calories=150,
                    protein=15,
                    carbs=12,
                    fats=4
                ),
            ]
            daily_plans.append(DayMealPlan(day=day, meals=meals))
            
        return MealPlanResponse(items=daily_plans)
