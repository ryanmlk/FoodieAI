# FoodieAI App - Features & Screens Documentation

## 📱 Screen Flow

```
Welcome Screen
     ↓
Gender Selection
     ↓
Personal Information (Age, Height, Weight)
     ↓
Activity Level
     ↓
Dietary Preference
     ↓
Calculating Screen (with animation)
     ↓
Nutrition Results
     ↓
Weekly Meal Plan
```

## 🎨 UI/UX Features

### 1. Welcome Screen
- **Elements:**
  - Animated app logo with shadow effect
  - App title "FoodieAI" with fade-in animation
  - Subtitle explaining the app's purpose
  - Three feature cards (Custom Meals, Track Nutrition, Stay Healthy)
  - "Get Started" button with slide animation
  
- **Animations:**
  - Logo scales in with fade effect
  - Title and subtitle slide up from bottom
  - Feature cards appear sequentially
  - Button slides up from bottom
  
- **Transitions:**
  - Slide transition to Gender Selection screen

### 2. Gender Selection Screen
- **Elements:**
  - Progress indicator (20% complete)
  - Title: "What's your gender?"
  - Description text
  - Male/Female selection cards with icons
  - Continue button
  
- **Animations:**
  - Progress bar slides in from left
  - Title and description fade in with slide up
  - Selection cards slide in from left sequentially
  - Selected card highlights with color change
  
- **Interactions:**
  - Tap cards to select
  - Selected card shows check mark
  - Color changes on selection

### 3. Personal Information Screen
- **Elements:**
  - Progress indicator (40% complete)
  - Title: "Tell us about yourself"
  - Three input fields (Age, Height, Weight)
  - Form validation
  - Continue button
  
- **Animations:**
  - Progress bar updates
  - Input fields slide in from left sequentially
  - Validation errors shake animation
  
- **Validation:**
  - Age: 10-120 years
  - Height: 100-250 cm
  - Weight: 30-300 kg

### 4. Activity Level Screen
- **Elements:**
  - Progress indicator (60% complete)
  - Title: "How active are you?"
  - Five activity level options:
    - Sedentary
    - Lightly Active
    - Moderately Active
    - Very Active
    - Extra Active
  - Continue button
  
- **Animations:**
  - Options appear sequentially
  - Selection animation with border and background color

### 5. Dietary Preference Screen
- **Elements:**
  - Progress indicator (80% complete)
  - Title: "Dietary preference"
  - Four dietary options:
    - Balanced
    - Vegetarian
    - Vegan
    - Keto
  - "Calculate My Plan" button
  
- **Animations:**
  - Options slide in sequentially
  - Selection feedback
  
- **Transition:**
  - Fade transition to calculating screen

### 6. Calculating Screen
- **Elements:**
  - Full-screen purple gradient background
  - Animated calculation icon
  - Title: "Calculating your nutritional goals"
  - Subtitle with explanation
  - Three pulsing dots
  
- **Animations:**
  - Icon pulses continuously (scale animation)
  - Dots fade in and out in sequence
  - 2.5 second calculation time
  
- **Purpose:**
  - Calculates BMR using Mifflin-St Jeor equation
  - Applies activity multiplier
  - Distributes macronutrients based on diet preference

### 7. Nutrition Results Screen
- **Elements:**
  - Purple gradient header with check icon
  - "Your Plan is Ready!" title
  - Main metric card showing daily calories
  - Three macro cards (Protein, Carbs, Fats)
  - Info card explaining the calculations
  - "View Weekly Meal Plan" button
  
- **Animations:**
  - Check icon scales in
  - Cards appear sequentially with fade and scale
  - Each element slides up from bottom
  
- **Visual Design:**
  - Color-coded macros:
    - Protein: Red (#FF6B6B)
    - Carbs: Teal (#4ECDC4)
    - Fats: Orange (#FFA726)

### 8. Weekly Meal Plan Screen
- **Elements:**
  - Purple gradient header
  - Daily nutritional targets
  - Horizontal day selector
  - Meal cards for selected day:
    - Breakfast (Orange)
    - Lunch (Green)
    - Dinner (Blue)
    - Snack (Purple)
  - Each meal shows calories and macros
  
- **Animations:**
  - Day tabs slide in from left
  - Meal cards appear sequentially
  - Selected day highlights with color
  - Smooth transitions when changing days
  
- **Interactions:**
  - Tap day to view that day's meals
  - Scroll through meal list
  - Settings button in header

## 🎯 State Management

### UserProvider (Provider pattern)
- Manages user profile data
- Handles nutrition calculations
- Provides data to all screens
- Methods:
  - `updateGender()`
  - `updateAge()`
  - `updateHeight()`
  - `updateWeight()`
  - `updateActivityLevel()`
  - `updateDietaryPreference()`
  - `calculateNutrition()`
  - `reset()`

## 🎨 Design System

### Colors
- **Primary**: #6C63FF (Purple) - Main brand color
- **Secondary**: #FF6584 (Pink) - Accents and highlights
- **Accent**: #4CAF50 (Green) - Success states
- **Background**: #F8F9FA (Light Gray)
- **Card Background**: White
- **Text Primary**: #2D3748 (Dark Gray)
- **Text Secondary**: #718096 (Medium Gray)
- **Border**: #E2E8F0 (Light Gray)

### Typography
- **Font Family**: Inter (Google Fonts)
- **Title**: 32px, Bold
- **Subtitle**: 16px, Regular
- **Body**: 14-16px, Regular
- **Button**: 16px, Semi-bold

### Spacing
- **Small**: 8px
- **Medium**: 16px
- **Large**: 24px
- **Extra Large**: 40px

### Border Radius
- **Small**: 12px
- **Medium**: 16px
- **Large**: 20px
- **Extra Large**: 30px

## 🔄 Navigation

### Transition Types
1. **Slide Transition**: Between onboarding screens
2. **Fade Transition**: To/from calculating screen
3. **Custom Page Routes**: Used throughout for smooth navigation

### Back Navigation
- All screens (except welcome and meal plan) have back button
- Back button in app bar (top left)

## 📊 Calculations

### BMR (Basal Metabolic Rate)
**Male:**
```
BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) + 5
```

**Female:**
```
BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) - 161
```

### Daily Calories
```
Daily Calories = BMR × Activity Multiplier
```

**Activity Multipliers:**
- Sedentary: 1.2
- Lightly Active: 1.375
- Moderately Active: 1.55
- Very Active: 1.725
- Extra Active: 1.9

### Macronutrients

**Balanced Diet:**
- Protein: 30% of calories ÷ 4 cal/g
- Carbs: 40% of calories ÷ 4 cal/g
- Fats: 30% of calories ÷ 9 cal/g

**Keto:**
- Protein: 25% ÷ 4
- Carbs: 5% ÷ 4
- Fats: 70% ÷ 9

**Vegetarian/Vegan:**
- Protein: 20% ÷ 4
- Carbs: 55% ÷ 4
- Fats: 25% ÷ 9

## 🚀 Performance Optimizations

1. **Lazy Loading**: Screens loaded on navigation
2. **Efficient Animations**: Using flutter_animate for optimized animations
3. **State Management**: Provider pattern for minimal rebuilds
4. **Image Optimization**: SVG icons for scalability
5. **Proper Disposal**: Controllers and listeners disposed properly

## 📱 Responsive Design

- All layouts use flexible widgets
- Breakpoints handled automatically by Flutter
- Text scales appropriately
- Cards adapt to screen width
- Spacing adjusts for different screen sizes

## 🎭 Animation Timing

- **Fade In**: 400-600ms
- **Slide**: 400-600ms
- **Scale**: 600ms
- **Delay Between Elements**: 100-200ms
- **Page Transitions**: 300ms
- **Button Press**: 200ms
- **Card Selection**: 200ms

## 🔮 Future Enhancements

1. **Backend Integration**
   - Connect to Python FastAPI server
   - Fetch real meal data from database
   - Sync user profiles

2. **Advanced Features**
   - Grocery list generation
   - Recipe details with instructions
   - Nutritional scanning (barcode)
   - Progress tracking graphs
   - Meal history

3. **Social Features**
   - Share meal plans
   - Community recipes
   - Friend challenges

4. **Integrations**
   - Fitness tracker sync
   - Health app integration
   - Smart home devices

5. **Personalization**
   - AI-powered meal suggestions
   - Allergen filters
   - Custom meal creation
   - Favorite meals

## 🧪 Testing Checklist

- [ ] All screens navigate correctly
- [ ] Animations run smoothly
- [ ] Form validation works
- [ ] Calculations are accurate
- [ ] State persists correctly
- [ ] Back navigation works
- [ ] No memory leaks
- [ ] Proper error handling
- [ ] Loading states work
- [ ] Responsive on different screen sizes
