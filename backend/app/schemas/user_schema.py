from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    VERY = "very"
    EXTRA = "extra"

class DietaryPreference(str, Enum):
    BALANCED = "balanced"
    KETO = "keto"
    VEGAN = "vegan"
    VEGETARIAN = "vegetarian"

class UserProfileRequest(BaseModel):
    gender: Gender
    age: int = Field(..., gt=0)
    height: float = Field(..., gt=0) # cm
    weight: float = Field(..., gt=0) # kg
    activity_level: ActivityLevel = ActivityLevel.SEDENTARY
    dietary_preference: DietaryPreference = DietaryPreference.BALANCED

class NutritionGoalsResponse(BaseModel):
    daily_calories: float
    protein: float
    carbs: float
    fats: float
