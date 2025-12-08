from pydantic import BaseModel
from typing import List

class Meal(BaseModel):
    name: str
    type: str # Breakfast, Lunch, Dinner, Snack
    calories: int
    protein: float
    carbs: float
    fats: float
    image_url: str = None

class DayMealPlan(BaseModel):
    day: str # Monday, Tuesday, etc.
    meals: List[Meal]

class MealPlanResponse(BaseModel):
    items: List[DayMealPlan]
